"""Motor desacoplado da interface: lógica de jogada + progresso persistente.

Este módulo não importa pygame, para permitir testes unitários sem gráficos.
O jogo de terminal (projeto08_forca.py) continua independente e inalterado.
"""
from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import tempfile

from projeto08_forca import (
    MAX_ERROS, escolher_palavra, categoria_da_palavra, venceu
)

VERSAO_SAVE = 2
VERSOES_COMPATIVEIS = {1, 2}
DEFAULT_CONFIG = {"musica": True, "efeitos": True}


def pasta_dados() -> Path:
    """Diretório persistente, fora da pasta temporária do .exe do PyInstaller."""
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", str(Path.home())))
        return base / "ForcaAmazonica"
    return Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share"))) / "ForcaAmazonica"


def caminho_save() -> Path:
    return pasta_dados() / "progresso.json"


def novo_estado(rodada=1, vitorias=0, pontuacao=0, sequencia_atual=0, melhor_sequencia=0) -> dict:
    if rodada < 1:
        raise ValueError("Rodada deve ser positiva")
    if min(vitorias, pontuacao, sequencia_atual, melhor_sequencia) < 0:
        raise ValueError("Placar inválido")
    palavra, dica = escolher_palavra(rodada)
    return {
        "rodada": rodada,
        "vitorias": vitorias,
        "pontuacao": pontuacao,
        "palavra": palavra,
        "dica": dica,
        "categoria": categoria_da_palavra(palavra),
        "acertadas": [],
        "erradas": [],
        "vidas": MAX_ERROS,
        "finalizada": False,
        "mensagem": "Descubra o nome amazônico, letra por letra!",
        "sequencia_atual": sequencia_atual,
        "melhor_sequencia": max(melhor_sequencia, sequencia_atual),
        "combo_titulo": "",
    }


def _mensagem_combo(estado: dict) -> str:
    if estado["sequencia_atual"] == 8:
        estado["combo_titulo"] = "INCRÍVEL!"
        return " INCRÍVEL! 8 vitórias seguidas!"
    if estado["sequencia_atual"] == 4:
        estado["combo_titulo"] = "EXCELENTE!"
        return " EXCELENTE! 4 vitórias seguidas!"
    estado["combo_titulo"] = ""
    return ""


def tentar_letra(estado: dict, letra: str) -> str:
    """Devolve acerto, erro, vitoria, derrota, repetida ou invalida."""
    if estado["finalizada"]:
        return "finalizada"
    letra = letra.strip().lower()
    if len(letra) != 1 or not ("a" <= letra <= "z"):
        estado["mensagem"] = "Digite apenas uma letra de A a Z."
        return "invalida"
    if letra in estado["acertadas"] or letra in estado["erradas"]:
        estado["mensagem"] = "Essa letra já foi usada. Nenhuma vida perdida!"
        return "repetida"
    if letra in estado["palavra"]:
        estado["acertadas"].append(letra)
        estado["mensagem"] = f"Muito bem! A letra {letra.upper()} está na palavra."
        if venceu(estado["palavra"], estado["acertadas"]):
            pontos = 10 + 5 * estado["vidas"]
            estado["pontuacao"] += pontos
            estado["vitorias"] += 1
            estado["sequencia_atual"] += 1
            estado["melhor_sequencia"] = max(estado["melhor_sequencia"], estado["sequencia_atual"])
            bonus = _mensagem_combo(estado)
            estado["finalizada"] = True
            estado["mensagem"] = (
                f"VITÓRIA! +{pontos} pontos. Nome revelado! ENTER: próxima rodada."
                f"{bonus}"
            )
            return "vitoria"
        return "acerto"
    estado["erradas"].append(letra)
    estado["vidas"] -= 1
    if estado["vidas"] == 0:
        estado["finalizada"] = True
        estado["sequencia_atual"] = 0
        estado["combo_titulo"] = ""
        estado["mensagem"] = f"Fim das vidas! Resposta: {estado['palavra'].upper()}. ENTER: continuar."
        return "derrota"
    estado["mensagem"] = f"A letra {letra.upper()} não aparece. Continue tentando!"
    return "erro"


def proxima_rodada(estado: dict) -> dict:
    if not estado["finalizada"]:
        raise ValueError("Termine a rodada antes de continuar")
    return novo_estado(
        estado["rodada"] + 1,
        estado["vitorias"],
        estado["pontuacao"],
        estado.get("sequencia_atual", 0),
        estado.get("melhor_sequencia", 0),
    )


def _validar_estado(dados) -> dict:
    """Não confia cegamente em JSON alterado, incompleto ou de versão antiga."""
    if not isinstance(dados, dict):
        raise ValueError("Estado não é um objeto")
    rodada = dados.get("rodada")
    vitorias = dados.get("vitorias")
    pontuacao = dados.get("pontuacao")
    if any(type(valor) is not int or valor < 0 for valor in (vitorias, pontuacao)):
        raise ValueError("Placar inválido")
    if type(rodada) is not int or rodada < 1 or rodada > 10_000_000:
        raise ValueError("Rodada inválida")
    if vitorias > rodada or pontuacao > vitorias * (10 + 5 * MAX_ERROS):
        raise ValueError("Placar inconsistente")

    sequencia_atual = dados.get("sequencia_atual", 0)
    melhor_sequencia = dados.get("melhor_sequencia", sequencia_atual)
    if any(type(valor) is not int or valor < 0 for valor in (sequencia_atual, melhor_sequencia)):
        raise ValueError("Sequências inválidas")
    if sequencia_atual > vitorias or melhor_sequencia < sequencia_atual:
        raise ValueError("Sequências inconsistentes")

    estado = novo_estado(rodada, vitorias, pontuacao, sequencia_atual, melhor_sequencia)
    palavra = estado["palavra"]
    if dados.get("palavra") != palavra:
        raise ValueError("Palavra incompatível com a rodada (catálogo alterado?)")
    certas = dados.get("acertadas")
    erradas = dados.get("erradas")
    if not isinstance(certas, list) or not isinstance(erradas, list):
        raise ValueError("Listas de letras inválidas")
    todas = certas + erradas
    if (len(todas) > 26 or len(set(map(str, todas))) != len(todas)
            or any(not isinstance(c, str) or len(c) != 1 or not ('a' <= c <= 'z') for c in todas)):
        raise ValueError("Letras inválidas ou duplicadas")
    if any(c not in palavra for c in certas) or any(c in palavra for c in erradas):
        raise ValueError("Acertos/erros incompatíveis com a palavra")
    if len(erradas) > MAX_ERROS:
        raise ValueError("Vidas inválidas")
    fim = venceu(palavra, certas) or len(erradas) == MAX_ERROS
    if bool(dados.get("finalizada")) != fim:
        raise ValueError("Estado final inconsistente")
    estado["acertadas"] = certas
    estado["erradas"] = erradas
    estado["vidas"] = MAX_ERROS - len(erradas)
    estado["finalizada"] = fim
    mensagem = dados.get("mensagem", estado["mensagem"])
    estado["mensagem"] = mensagem[:220] if isinstance(mensagem, str) else estado["mensagem"]
    combo_titulo = dados.get("combo_titulo", "")
    if isinstance(combo_titulo, str):
        estado["combo_titulo"] = combo_titulo[:40]
    if fim and venceu(palavra, certas) and not estado["combo_titulo"]:
        _mensagem_combo(estado)
    return estado


def salvar_jogo(estado: dict, config: dict | None = None, destino: Path | None = None) -> Path:
    """Escrita atômica: grava temporário, depois troca o arquivo do save."""
    destino = Path(destino) if destino is not None else caminho_save()
    destino.parent.mkdir(parents=True, exist_ok=True)
    config = config or DEFAULT_CONFIG
    conteudo = {
        "versao": VERSAO_SAVE,
        "atualizado_em": datetime.now().isoformat(timespec="seconds"),
        "estado": _validar_estado(estado),
        "config": {chave: bool(config.get(chave, True)) for chave in DEFAULT_CONFIG},
    }
    temporario = None
    try:
        with tempfile.NamedTemporaryFile(
            'w', encoding='utf-8', dir=destino.parent,
            prefix='.progresso_', suffix='.tmp', delete=False
        ) as arq:
            temporario = Path(arq.name)
            json.dump(conteudo, arq, ensure_ascii=False, indent=2)
            arq.flush()
            os.fsync(arq.fileno())
        os.replace(temporario, destino)
    finally:
        if temporario is not None and temporario.exists():
            temporario.unlink()
    return destino


def carregar_jogo(origem: Path | None = None):
    """Retorna (estado, config, mensagem); save ruim não impede abrir o jogo."""
    origem = Path(origem) if origem is not None else caminho_save()
    if not origem.is_file():
        return novo_estado(), DEFAULT_CONFIG.copy(), "Nova aventura! O jogo salvará automaticamente."
    try:
        with origem.open('r', encoding='utf-8') as arq:
            dados = json.load(arq)
        versao = dados.get('versao')
        if type(versao) is not int or versao not in VERSOES_COMPATIVEIS:
            raise ValueError('Versão de salvamento incompatível')
        estado = _validar_estado(dados['estado'])
        bruto = dados.get('config', {})
        if not isinstance(bruto, dict):
            bruto = {}
        config = {k: bool(bruto.get(k, True)) for k in DEFAULT_CONFIG}
        return estado, config, 'Seu progresso anterior foi recuperado!'
    except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError) as erro:
        return novo_estado(), DEFAULT_CONFIG.copy(), f'Não foi possível recuperar o save: {erro}'
