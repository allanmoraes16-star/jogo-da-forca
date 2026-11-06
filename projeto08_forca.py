"""Projeto 08 – Forca Amazônica | CETAM Python 80h.

Integrantes: __________________________________________
Preencha os nomes antes de entregar à professora.

Versão principal em terminal: cumpre RF01–RF07 e RN01–RN06.
Requer apenas Python 3; nenhuma biblioteca externa.
"""

# RF01: catálogo de palavras e dicas armazenado em uma tupla de tuplas.
# Mantemos as respostas em a-z, sem espaços, hífens ou acentos.
# Cada categoria é uma tupla de pares (palavra, dica): ótima prática de estruturas de dados.
PEIXES = (
    ('tambaqui', 'Peixe de corpo arredondado, comum assado nas refeições do Amazonas.'),
    ('pirarucu', 'Peixe gigante de água doce, conhecido pelas escamas grandes e pela respiração aérea.'),
    ('tucunare', 'Predador de água doce muito procurado na pesca esportiva, de cores vistosas.'),
    ('jaraqui', 'Peixe pequeno bastante presente nas feiras e refeições de Manaus.'),
    ('matrinxa', 'Peixe de escamas, corpo alongado e carne apreciada, frequentemente preparado na brasa.'),
    ('pirapitinga', 'Peixe aparentado ao tambaqui, de corpo alto e nadadeiras avermelhadas quando jovem.'),
    ('aracu', 'Peixe de escamas que costuma se alimentar de vegetais e matéria orgânica em rios.'),
    ('pacu', 'Peixe de corpo arredondado, conhecido por consumir frutos e sementes que caem na água.'),
    ('curimata', 'Peixe de escamas que se alimenta de detritos e é comum nos mercados ribeirinhos.'),
    ('bodo', 'Peixe de couro rígido, com placas no corpo e boca em forma de ventosa; também chamado acari.'),
    ('piranha', 'Peixe famoso por seus dentes afiados e pela mordida forte.'),
    ('aruana', 'Peixe alongado que salta fora da água para capturar presas próximas à superfície.'),
    ('surubim', 'Bagre de grande porte, sem escamas, com manchas ou listras escuras.'),
    ('caparari', 'Bagre amazônico de manchas marcadas, conhecido como surubim-tigre.'),
    ('piraiba', 'Um dos maiores bagres dos rios amazônicos; juvenis recebem o nome de filhote.'),
    ('pirarara', 'Bagre de grande porte, famoso pela cauda e nadadeiras de tons avermelhados.'),
    ('dourada', 'Bagre migrador que percorre longas distâncias pelos rios da bacia amazônica.'),
    ('mapara', 'Bagre de corpo comprimido e carne bastante apreciada em algumas regiões amazônicas.'),
    ('piramutaba', 'Bagre migratório de grande importância na pesca do estuário amazônico.'),
    ('branquinha', 'Peixe pequeno e prateado, comum em cardumes de rios e lagos.'),
    ('mandube', 'Bagre de corpo relativamente liso, encontrado em águas amazônicas.'),
    ('cuiucuiu', 'Bagre encouraçado de grande porte, com espinhos e placas ósseas.'),
    ('apapa', 'Peixe de escamas brilhantes e corpo comprimido, também chamado de sardinha-dourada.'),
    ('bicuda', 'Predador de corpo longo e focinho pontudo, conhecido por ataques rápidos.'),
    ('traira', 'Peixe predador de água doce que costuma ficar à espreita da presa.'),
    ('jacunda', 'Peixe alongado da família dos ciclídeos, comum em igarapés e águas calmas.'),
    ('acara', 'Nome popular de vários ciclídeos, peixes de corpo lateralmente achatado.'),
    ('pescada', 'Peixe valorizado pela carne branca, encontrado nos mercados de pescado amazônicos.'),
    ('tamoata', 'Peixe de placas ósseas, resistente e capaz de sobreviver em água pouco oxigenada.'),
    ('jau', 'Bagre grande e robusto, conhecido pelo corpo escuro e pela cabeça larga.'),
    ('jundia', 'Nome comum de certos bagres de água doce, com longos barbilhões.'),
    ('apaiari', 'Ciclídeo amazônico apreciado em aquários, conhecido também como oscar.'),
)

FRUTAS = (
    ('cupuacu', 'Fruto marrom, de polpa branca e aromática, usado em bombons, doces e sucos.'),
    ('acai', 'Fruto pequeno e roxo de palmeira, transformado em bebida e polpa muito consumida no Norte.'),
    ('tucuma', 'Fruto de palmeira com polpa alaranjada, muito usado em sanduíches de Manaus.'),
    ('pupunha', 'Fruto de palmeira que costuma ser cozido e servido com café.'),
    ('bacaba', 'Frutinho escuro de palmeira, batido para produzir bebida semelhante à do açaí.'),
    ('buriti', 'Fruto de palmeira de áreas úmidas, com polpa alaranjada rica em pigmentos.'),
    ('tapereba', 'Frutinha amarela e ácida, muito usada em suco e sorvete; também chamada cajá.'),
    ('camucamu', 'Fruta pequena e azedinha de áreas alagáveis, conhecida pela vitamina C.'),
    ('guarana', 'Fruto cuja semente é usada em bebidas; ao abrir, lembra um olho.'),
    ('abiu', 'Fruta geralmente amarela, de polpa translúcida e sabor adocicado.'),
    ('aracaboi', 'Fruta muito aromática e ácida, parente das goiabas, indicada para sucos.'),
    ('bacuri', 'Fruto de casca grossa e polpa branca, apreciado em doces e cremes.'),
    ('biriba', 'Fruto de casca amarela com saliências, de polpa clara e bastante doce.'),
    ('inga', 'Fruto em vagem que guarda sementes envoltas por polpa branca e adocicada.'),
    ('cacau', 'Fruto cujas sementes dão origem ao chocolate e cuja polpa rende sucos.'),
    ('castanha', 'Semente retirada do ouriço de árvore amazônica gigante; também chamada do-brasil.'),
    ('cubiu', 'Fruto alaranjado ou vermelho, parecido com um tomate, empregado em molhos e sucos.'),
    ('cupui', 'Fruto menor, parente do cupuaçu, com polpa usada em preparações regionais.'),
    ('uxi', 'Fruto de polpa amarela e oleosa, comido ao natural ou usado em cremes.'),
    ('piquia', 'Fruto com polpa amarela e aromática, conhecido pelo cheiro forte quando cozido.'),
    ('pataua', 'Fruto escuro de palmeira usado para bebida, óleo e preparações alimentícias.'),
    ('murici', 'Frutinha amarela de aroma marcante, utilizada em sucos e sorvetes.'),
    ('jenipapo', 'Fruto que pode produzir pigmento azul-escuro, usado em pinturas corporais.'),
    ('mapati', 'Fruto que cresce em cachos e também é chamado de uva-da-amazônia.'),
    ('mari', 'Fruto de casca amarela e polpa oleosa, consumido em algumas áreas amazônicas.'),
    ('pajura', 'Fruto regional de casca firme e polpa comestível, conhecido em comunidades amazônicas.'),
    ('purui', 'Fruto silvestre amazônico de polpa comestível, citado em estudos de fruteiras regionais.'),
    ('sorva', 'Fruto de árvore que também fornece látex; pode ser consumido ao amadurecer.'),
    ('bacupari', 'Fruto de casca amarelada, parente do mangostão, com polpa branca adocicada.'),
    ('marimari', 'Fruto de árvore amazônica, com polpa comestível, citado entre fruteiras da região.'),
    ('jatoba', 'Fruto em vagem de casca dura cuja polpa farinácea pode ser aproveitada.'),
    ('pitomba', 'Fruta pequena de casca firme e polpa translúcida ao redor do caroço.'),
)

ANIMAIS = (
    ('onca', 'Grande felino pintado, predador de topo da floresta amazônica.'),
    ('ariranha', 'Mamífero aquático sociável, semelhante à lontra, que caça peixes em grupo.'),
    ('boto', 'Mamífero de rio famoso pela coloração rosada e pelas lendas da região.'),
    ('peixeboi', 'Mamífero aquático herbívoro que vive em rios amazônicos; não é um peixe.'),
    ('uacari', 'Macaco amazônico de face avermelhada e cauda relativamente curta.'),
    ('guariba', 'Macaco conhecido por vocalizações graves e muito altas; também chamado bugio.'),
    ('preguica', 'Mamífero arborícola de movimentos lentos, que passa muito tempo pendurado.'),
    ('macacoaranha', 'Primata de membros longos e cauda preênsil, muito ágil no alto das árvores.'),
    ('anta', 'Maior mamífero terrestre nativo do Brasil, com focinho flexível.'),
    ('capivara', 'Grande roedor semiaquático que vive próximo a rios e lagos.'),
    ('cutia', 'Roedor de pernas relativamente longas que enterra sementes na floresta.'),
    ('paca', 'Roedor noturno de corpo robusto e fileiras de manchas claras.'),
    ('quati', 'Mamífero de focinho comprido e cauda anelada, que busca alimento no chão.'),
    ('tamandua', 'Mamífero de focinho alongado, especializado em comer formigas e cupins.'),
    ('tatu', 'Mamífero terrestre protegido por uma carapaça formada de placas.'),
    ('pacarana', 'Roedor florestal raro e robusto, com manchas claras pelo corpo.'),
    ('jaguatirica', 'Felino menor que a onça-pintada, de pelagem manchada e hábitos discretos.'),
    ('sucuri', 'Cobra de grande porte que vive perto da água e mata presas por constrição.'),
    ('jacare', 'Réptil de focinho alongado e pele escamosa que habita rios e lagos.'),
    ('tracaja', 'Quelônio de água doce muito conhecido nas comunidades ribeirinhas.'),
    ('jabuti', 'Quelônio terrestre de casco alto, diferente das tartarugas aquáticas.'),
    ('arara', 'Ave de bico forte, cauda longa e plumagem de cores intensas.'),
    ('tucano', 'Ave de bico enorme e colorido que ajuda a dispersar sementes.'),
    ('harpia', 'Ave de rapina poderosa que caça mamíferos nas copas das árvores.'),
    ('mutum', 'Ave de floresta, geralmente escura, da mesma família dos jacus.'),
    ('jacamim', 'Ave terrestre da floresta, de pernas longas, que vive em grupos.'),
    ('cigana', 'Ave conhecida como hoatzim, de cheiro marcante e digestão por fermentação.'),
    ('aracari', 'Ave da família dos tucanos, geralmente menor e de bico colorido.'),
    ('surucucu', 'Grande serpente venenosa da floresta, de presas longas e cauda espinhosa.'),
    ('jiboia', 'Serpente não venenosa que captura presas por constrição.'),
    ('caititu', 'Mamífero parecido com um porco-do-mato, de porte menor que a queixada.'),
    ('queixada', 'Porco-do-mato que anda em bandos numerosos e tem uma área clara perto da boca.'),
)

# Intercalamos as três categorias: peixe, fruta, animal, peixe, fruta, animal...
# Como há 32 itens em cada uma, formamos exatamente 96 rodadas sem repetir.
PALAVRAS = tuple(item for trio in zip(PEIXES, FRUTAS, ANIMAIS) for item in trio)


def categoria_da_palavra(palavra):
    """Retorna o nome da categoria sem modificar o formato de PALAVRAS."""
    if palavra in {nome for nome, _ in PEIXES}:
        return "PEIXES"
    if palavra in {nome for nome, _ in FRUTAS}:
        return "FRUTAS E SEMENTES"
    if palavra in {nome for nome, _ in ANIMAIS}:
        return "OUTROS ANIMAIS"
    raise ValueError(f"Palavra fora do catálogo: {palavra}")

MAX_ERROS = 6


def escolher_palavra(numero_rodada):
    """RF02: retorna (palavra, dica), reiniciando após percorrer 96 palavras.

    Exemplo: rodada 1 -> índice 0; rodada 97 -> índice 0.
    """
    if numero_rodada < 1:
        raise ValueError("O número da rodada deve ser pelo menos 1.")
    indice = (numero_rodada - 1) % len(PALAVRAS)
    return PALAVRAS[indice]


def montar_exibicao(palavra, acertadas):
    """RF03: retorna a palavra com espaços e '_' para letras ocultas."""
    exibicao = []
    for letra in palavra:
        if letra in acertadas:
            exibicao.append(letra)
        else:
            exibicao.append("_")
    return " ".join(exibicao)


def venceu(palavra, acertadas):
    """RF04: True somente quando todas as letras estão descobertas."""
    for letra in palavra:
        if letra not in acertadas:
            return False
    return True


def ler_letra(tentadas):
    """RF05: valida exatamente uma letra a-z, ainda não tentada."""
    while True:
        letra = input("Digite uma letra: ").strip().lower()

        # isalpha() sozinho também aceita letras acentuadas, como 'á'.
        if len(letra) != 1 or not ("a" <= letra <= "z"):
            print("Digite apenas UMA letra (de a a z).")
        elif letra in tentadas:
            print("Você já tentou essa letra!")
        else:
            return letra


def jogar_rodada(numero_rodada):
    """RF06: executa uma rodada, retornando (ganhou, pontos)."""
    palavra, dica = escolher_palavra(numero_rodada)
    acertadas = []
    erradas = []
    vidas = MAX_ERROS

    print(f"\n=== RODADA {numero_rodada} ===")
    print(f"Categoria: {categoria_da_palavra(palavra)}")
    print(f"Dica: {dica}")

    # O while termina por vitória OU por esgotamento das seis vidas.
    while vidas > 0 and not venceu(palavra, acertadas):
        print(f"\nPalavra: {montar_exibicao(palavra, acertadas)}")
        print("Vidas:", " ".join(["O"] * vidas + ["X"] * (MAX_ERROS - vidas)))
        print(f"Letras erradas: {erradas}")

        # A soma cria a lista de todas as letras já digitadas.
        letra = ler_letra(acertadas + erradas)
        if letra in palavra:
            acertadas.append(letra)
            print("Acertou!")
        else:
            erradas.append(letra)
            vidas -= 1
            print("Errou!")

    print(f"\nPalavra: {montar_exibicao(palavra, acertadas)}")
    if venceu(palavra, acertadas):
        pontos = 10 + 5 * vidas
        print(f"Parabéns! Palavra: {palavra}. +{pontos} pontos!")
        return True, pontos

    print(f"Fim das vidas! A palavra era '{palavra}'. +0 pontos.")
    return False, 0


def principal():
    """RF07: controla as rodadas, vitórias e pontuação acumulada."""
    rodadas = 0
    vitorias = 0
    pontuacao = 0

    print("=== FORCA AMAZÔNICA ===")
    print(f"Descubra {len(PALAVRAS)} palavras da Amazônia. Você tem 6 vidas por rodada!")

    while True:
        rodadas += 1
        ganhou, pontos = jogar_rodada(rodadas)
        if ganhou:
            vitorias += 1
        pontuacao += pontos

        print(f"\nPlacar: {vitorias} vitória(s) | {pontuacao} ponto(s)")
        while True:
            resposta = input("Jogar outra rodada? (s/n): ").strip().lower()
            if resposta in ("s", "n"):
                break
            print("Responda apenas 's' ou 'n'.")

        if resposta == "n":
            break

    print("\n=== PLACAR FINAL ===")
    print(f"Rodadas: {rodadas}")
    print(f"Vitórias: {vitorias}")
    print(f"Pontuação total: {pontuacao}")


# Boa prática: importar o arquivo em testes sem iniciar o jogo automaticamente.
if __name__ == "__main__":
    principal()
