"""Extensão opcional: Forca Amazônica com interface gráfica em Pygame.

Instalação (Python 3.14): python -m pip install --only-binary=:all: pygame-ce
Execução:   python forca_pygame.py

Reutiliza as regras RF02–RF04 do projeto08_forca.py.
Esta versão gráfica NÃO é exigida no projeto original do CETAM.
"""

try:
    import pygame
except ImportError as erro:
    raise SystemExit(
        "Pygame não instalado. Execute: python -m pip install --only-binary=:all: pygame-ce"
    ) from erro

from projeto08_forca import MAX_ERROS, PALAVRAS, categoria_da_palavra, escolher_palavra, montar_exibicao, venceu

LARGURA, ALTURA = 1100, 760
FPS = 60
VERDE_ESCURO = (0, 60, 45)
VERDE = (21, 122, 85)
MENTA = (159, 201, 181)
CREME = (246, 246, 232)
AMARELO = (255, 200, 87)
VERMELHO = (224, 100, 90)
BRANCO = (255, 255, 255)
AZUL_RIO = (47, 140, 155)
CINZA = (93, 108, 106)

LINHAS_TECLADO = ("qwertyuiop", "asdfghjkl", "zxcvbnm")


def criar_estado(rodada, vitorias=0, pontuacao=0):
    """Inicializa os dados de uma rodada; sem dependência de tela."""
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
        "mensagem": "Escolha uma letra no teclado ou na tela.",
    }


def tentar_letra(estado, letra):
    """Atualiza o jogo depois de uma tentativa válida a–z."""
    if estado["finalizada"]:
        return
    letra = letra.strip().lower()
    if len(letra) != 1 or not ("a" <= letra <= "z"):
        estado["mensagem"] = "Use apenas uma letra de a a z."
        return
    if letra in estado["acertadas"] + estado["erradas"]:
        estado["mensagem"] = "Letra repetida: tente outra, sem perder vida."
        return

    if letra in estado["palavra"]:
        estado["acertadas"].append(letra)
        estado["mensagem"] = f"Boa! A letra '{letra}' está na palavra."
    else:
        estado["erradas"].append(letra)
        estado["vidas"] -= 1
        estado["mensagem"] = f"A letra '{letra}' não aparece."

    if venceu(estado["palavra"], estado["acertadas"]):
        pontos = 10 + 5 * estado["vidas"]
        estado["pontuacao"] += pontos
        estado["vitorias"] += 1
        estado["finalizada"] = True
        estado["mensagem"] = f"VITÓRIA! +{pontos} pontos. Pressione ENTER para continuar."
    elif estado["vidas"] == 0:
        estado["finalizada"] = True
        estado["mensagem"] = (
            f"Fim das vidas! Palavra: {estado['palavra']}. Pressione ENTER."
        )


def texto(tela, fonte, conteudo, x, y, cor=VERDE_ESCURO, centro=False):
    superficie = fonte.render(str(conteudo), True, cor)
    posicao = superficie.get_rect()
    if centro:
        posicao.center = (x, y)
    else:
        posicao.topleft = (x, y)
    tela.blit(superficie, posicao)


def texto_quebrado(tela, fonte, conteudo, x, y, max_largura, cor=VERDE_ESCURO):
    """Quebra a dica nos espaços: as linhas não saem do cartão."""
    linha = ""
    for palavra in conteudo.split():
        teste = (linha + " " + palavra).strip()
        if linha and fonte.size(teste)[0] > max_largura:
            texto(tela, fonte, linha, x, y, cor)
            y += fonte.get_linesize() + 5
            linha = palavra
        else:
            linha = teste
    if linha:
        texto(tela, fonte, linha, x, y, cor)


def desenhar_fundo(tela):
    """Camadas de cenário feitas apenas com primitivas geométricas."""
    tela.fill((221, 238, 215))
    pygame.draw.circle(tela, AMARELO, (980, 70), 66)
    pygame.draw.polygon(tela, (108, 168, 121), [(0, 700), (180, 110), (430, 700)])
    pygame.draw.polygon(tela, (68, 146, 105), [(540, 710), (890, 130), (1100, 710)])
    pygame.draw.rect(tela, AZUL_RIO, (0, 690, LARGURA, 70))
    for i in range(12):
        pygame.draw.line(tela, (151, 221, 213), (i * 105, 710), (i * 105 + 40, 710), 3)


def desenhar_arvore(tela, vidas):
    """Representa as seis vidas por seis folhas na árvore amazônica."""
    pygame.draw.line(tela, (115, 74, 44), (900, 595), (900, 385), 27)
    pygame.draw.line(tela, (115, 74, 44), (900, 465), (846, 417), 12)
    pygame.draw.line(tela, (115, 74, 44), (900, 450), (949, 406), 12)
    posicoes = [(820, 386), (866, 345), (917, 330), (964, 370), (829, 438), (955, 430)]
    for i, (x, y) in enumerate(posicoes):
        if i < vidas:
            cor = (48 + i * 8, 138 + i * 7, 68)
            pygame.draw.ellipse(tela, cor, (x - 28, y - 17, 58, 37))
            pygame.draw.line(tela, (212, 235, 157), (x - 15, y), (x + 17, y), 2)
        else:
            pygame.draw.ellipse(tela, (182, 193, 171), (x - 28, y - 17, 58, 37), 2)


def desenhar_teclado(tela, estado, fonte):
    """Retorna as áreas clicáveis (pygame.Rect, letra)."""
    areas = []
    for linha, letras in enumerate(LINHAS_TECLADO):
        largura_linha = len(letras) * 53 - 7
        inicio = 375 - largura_linha // 2
        y = 486 + linha * 60
        for indice, letra in enumerate(letras):
            area = pygame.Rect(inicio + indice * 53, y, 46, 48)
            if letra in estado["acertadas"]:
                cor = VERDE
                tinta = BRANCO
            elif letra in estado["erradas"]:
                cor = (187, 194, 187)
                tinta = CINZA
            else:
                cor = CREME
                tinta = VERDE_ESCURO
            pygame.draw.rect(tela, cor, area, border_radius=9)
            pygame.draw.rect(tela, MENTA, area, 2, border_radius=9)
            texto(tela, fonte, letra.upper(), area.centerx, area.centery, tinta, centro=True)
            areas.append((area, letra))
    return areas


def desenhar(tela, estado, fontes):
    principal, media, pequena = fontes
    desenhar_fundo(tela)
    texto(tela, principal, "FORCA AMAZÔNICA", 39, 36, VERDE_ESCURO)
    pygame.draw.rect(tela, (235, 244, 232), (35, 112, 680, 591), border_radius=23)
    pygame.draw.rect(tela, (235, 244, 232), (732, 112, 334, 591), border_radius=23)
    texto(tela, media, f"RODADA {estado['rodada']}", 66, 145, VERDE)
    texto(tela, pequena, f"CATEGORIA: {estado['categoria']}  |  {len(PALAVRAS)} PALAVRAS", 66, 199, CINZA)
    texto(tela, pequena, "DICA", 66, 226, CINZA)
    texto_quebrado(tela, pequena, estado["dica"], 66, 254, 606, VERDE_ESCURO)

    exibicao = montar_exibicao(estado["palavra"], estado["acertadas"])
    fonte_palavra = principal
    # Palavras mais longas não devem ultrapassar a largura do cartão.
    if principal.size(exibicao)[0] > 605:
        fonte_palavra = media
    texto(tela, fonte_palavra, exibicao, 375, 354, VERDE_ESCURO, centro=True)
    texto(tela, media, f"Vidas: {estado['vidas']} / {MAX_ERROS}", 67, 387, VERDE)
    texto(tela, pequena, "Erradas: " + ", ".join(estado["erradas"] or ["nenhuma"]), 67, 424)
    texto_quebrado(tela, pequena, estado["mensagem"], 67, 451, 604, VERDE_ESCURO)
    areas = desenhar_teclado(tela, estado, media)

    texto(tela, media, "PLACAR", 768, 151, VERDE)
    texto(tela, pequena, f"Vitórias: {estado['vitorias']}", 768, 200)
    texto(tela, pequena, f"Pontos: {estado['pontuacao']}", 768, 235)
    texto(tela, pequena, "Cada erro remove uma folha", 768, 274, CINZA)
    desenhar_arvore(tela, estado["vidas"])

    if estado["finalizada"]:
        botao = pygame.Rect(761, 625, 276, 53)
        pygame.draw.rect(tela, VERDE, botao, border_radius=12)
        texto(tela, pequena, "PRÓXIMA RODADA (ENTER)", botao.centerx, botao.centery, BRANCO, centro=True)
    else:
        botao = None
        texto(tela, pequena, "ESC: sair  |  teclado ou mouse", 756, 647, CINZA)

    pygame.display.flip()  # Apresenta o frame completo na janela.
    return areas, botao


def principal_grafico():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Projeto 08 – Forca Amazônica")
    relogio = pygame.time.Clock()
    fontes = (
        pygame.font.SysFont("arial", 38, bold=True),
        pygame.font.SysFont("arial", 26, bold=True),
        pygame.font.SysFont("arial", 19),
    )
    estado = criar_estado(1)
    areas_teclado = []
    botao_proximo = None
    rodando = True

    while rodando:
        # 1. Processar eventos (o teclado/mouse pode mudar o estado).
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_RETURN and estado["finalizada"]:
                    estado = criar_estado(
                        estado["rodada"] + 1,
                        estado["vitorias"],
                        estado["pontuacao"],
                    )
                elif not estado["finalizada"]:
                    tentar_letra(estado, evento.unicode)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if estado["finalizada"]:
                    if botao_proximo is not None and botao_proximo.collidepoint(evento.pos):
                        estado = criar_estado(
                            estado["rodada"] + 1,
                            estado["vitorias"],
                            estado["pontuacao"],
                        )
                else:
                    for area, letra in areas_teclado:
                        if area.collidepoint(evento.pos):
                            tentar_letra(estado, letra)
                            break

        # 2. Renderizar o novo estado a cada frame.
        areas_teclado, botao_proximo = desenhar(tela, estado, fontes)
        # 3. Limitar frames para não sobrecarregar o computador.
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    principal_grafico()
