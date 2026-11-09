"""FORCA AMAZÔNICA DELUXE — jogo Pygame com progresso e painel textual animado.

Execute: python forca_pygame.py
Dependências: pygame-ce.

ESC: salva e sai   ENTER: próxima rodada (quando terminar)
F5: salvar         F6: pedir novo jogo
F8: ligar/desligar música   F9: ligar/desligar efeitos
"""
from __future__ import annotations

from pathlib import Path
import math

try:
    import pygame
except ImportError as erro:
    raise SystemExit('Instale o Pygame: python -m pip install pygame-ce') from erro

from projeto08_forca import MAX_ERROS, montar_exibicao
from motor_grafico import (
    carregar_jogo, salvar_jogo, novo_estado, tentar_letra,
    proxima_rodada
)

LARGURA, ALTURA = 1200, 800
FPS = 30  # 30 quadros/segundo para evitar uso desnecessário de CPU no notebook.
VERDE_PROFUNDO = (8, 49, 42)
VERDE = (15, 108, 78)
VERDE_CLARO = (118, 195, 143)
MENTA = (189, 224, 198)
BRANCO = (253, 254, 249)
CREME = (240, 245, 226)
OURO = (244, 191, 81)
RUBI = (202, 82, 68)
CINZA = (82, 107, 95)
AZUL = (47, 125, 150)

BASE = Path(__file__).resolve().parent
ASSETS = BASE / 'assets'
SOM = ASSETS / 'sons'
TECLADO = ('QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM')


def texto(tela, fonte, conteudo, x, y, cor=VERDE_PROFUNDO, centro=False):
    imagem = fonte.render(str(conteudo), True, cor)
    ret = imagem.get_rect()
    if centro:
        ret.center = (x,y)
    else:
        ret.topleft = (x,y)
    tela.blit(imagem,ret)


def escrever_linhas(tela, fonte, conteudo, x, y, largura, cor=VERDE_PROFUNDO, max_linhas=3):
    linha = ''
    linhas = []
    for palavra in conteudo.split():
        teste = (linha + ' ' + palavra).strip()
        if linha and fonte.size(teste)[0] > largura:
            linhas.append(linha)
            linha = palavra
        else:
            linha = teste
    if linha:
        linhas.append(linha)
    for parte in linhas[:max_linhas]:
        texto(tela,fonte,parte,x,y,cor)
        y += fonte.get_linesize() + 3


def retangulo(tela, area, cor, borda=0, raio=14):
    pygame.draw.rect(tela,cor,area,borda,border_radius=raio)


def criar_cenario():
    fundo = pygame.Surface((LARGURA,ALTURA)).convert()
    # Degradê vertical do céu ao rio (criado uma única vez).
    for y in range(ALTURA):
        t=y/ALTURA
        cor=(int(220-80*t), int(244-52*t), int(207-86*t))
        pygame.draw.line(fundo,cor,(0,y),(LARGURA,y))
    pygame.draw.circle(fundo,(252,224,145),(1080,95),90)
    pygame.draw.polygon(fundo,(92,163,121),[(0,650),(190,130),(370,650)])
    pygame.draw.polygon(fundo,(71,146,105),[(490,740),(950,170),(1200,740)])
    pygame.draw.polygon(fundo,(37,116,92),[(0,750),(0,300),(120,640),(315,240),(480,750)])
    pygame.draw.rect(fundo,(52,135,143),(0,747,LARGURA,53))
    for i in range(11):
        pygame.draw.line(fundo,(162,210,193),(i*120,780),(i*120+65,780),2)
    return fundo


class PainelDescoberta:
    """Painel de suspense e recompensa sem imagens externas."""
    def __init__(self):
        self.chave = None
        self.desbloqueado = False
        self.palavra = ''
        self.inicio = 0

    def carregar(self, estado):
        chave = (estado['palavra'], bool(estado['finalizada'] and estado['vidas'] > 0))
        if self.chave == chave:
            return
        self.chave = chave
        self.palavra = estado['palavra'].upper()
        self.desbloqueado = bool(estado['finalizada'] and estado['vidas'] > 0)
        self.inicio = pygame.time.get_ticks()

    def _cores_animadas(self, tempo):
        return (
            int(120 + 100 * (math.sin(tempo * 2.0) + 1) / 2),
            int(80 + 120 * (math.sin(tempo * 2.0 + 2.1) + 1) / 2),
            int(120 + 110 * (math.sin(tempo * 2.0 + 4.2) + 1) / 2),
        )

    def _desenhar_bloqueado(self, tela):
        area = pygame.Rect(822,296,319,303)
        retangulo(tela, area, (212, 232, 214), raio=8)
        retangulo(tela, area, VERDE_CLARO, borda=2, raio=8)
        tempo = pygame.time.get_ticks() / 1000.0
        desloc = math.sin(tempo * 5.2) * 9
        pulso = 1.0 + 0.05 * math.sin(tempo * 4.0)
        cor = self._cores_animadas(tempo)
        raio = int(90 * pulso)
        pygame.draw.circle(tela, cor, (982, 420 + int(desloc)), raio)
        pygame.draw.circle(tela, BRANCO, (982, 420 + int(desloc)), int(raio * 0.72))
        fonte_q = pygame.font.SysFont('arial', int(122 * pulso), bold=True)
        texto(tela, fonte_q, '?', 982, 412 + int(desloc), cor, centro=True)
        elevacao = int(math.sin(tempo * 5.2) * 4)
        texto(tela, FONTES['misterio'], 'MISTÉRIO AMAZÔNICO', 982, 548 + elevacao, cor, centro=True)

    def _quebrar_linhas(self, fonte, conteudo, largura):
        linhas = []
        linha = ''
        for palavra in conteudo.split():
            teste = (linha + ' ' + palavra).strip()
            if linha and fonte.size(teste)[0] > largura:
                linhas.append(linha)
                linha = palavra
            else:
                linha = teste
        if linha:
            linhas.append(linha)
        return linhas

    def _desenhar_descoberto(self, tela):
        area = pygame.Rect(822,296,319,303)
        retangulo(tela, area, (212, 232, 214), raio=8)
        tempo = (pygame.time.get_ticks() - self.inicio) / 1000.0
        cor = self._cores_animadas(tempo)
        brilho = self._cores_animadas(tempo + 0.7)
        progresso = min(1.0, (pygame.time.get_ticks() - self.inicio) / 700)
        easing = 1 - (1 - progresso) ** 3
        y0 = 325 + int((1 - easing) * 70)
        altura = 210
        faixa = pygame.Rect(840, y0, 283, altura)
        retangulo(tela, faixa, BRANCO, raio=18)
        retangulo(tela, faixa, cor, borda=3, raio=18)
        texto(tela, FONTES['mini'], 'PALAVRA DESCOBERTA', 982, y0 + 28, VERDE_PROFUNDO, centro=True)
        fonte = next((f for f in (FONTES['revelada'], FONTES['revelada_media'], FONTES['revelada_pequena'])
                      if f.size(self.palavra)[0] <= 238), FONTES['revelada_pequena'])
        linhas = [self.palavra]
        base_y = y0 + 95 - (len(linhas)-1) * 26
        oscil = int(math.sin(tempo * 6.0) * 4)
        for i, linha in enumerate(linhas[:3]):
            texto(tela, fonte, linha, 982, base_y + i * 52 + oscil, brilho if i % 2 == 0 else cor, centro=True)
        texto(tela, FONTES['mini'], 'RECOMPENSA DA RODADA', 982, y0 + altura - 24, CINZA, centro=True)

    def desenhar(self, tela):
        retangulo(tela, pygame.Rect(812,284,340,326), (226,241,221), raio=15)
        if not self.desbloqueado:
            self._desenhar_bloqueado(tela)
        else:
            self._desenhar_descoberto(tela)


class Audio:
    def __init__(self,config):
        self.config=config
        self.efeitos={}
        self.disponivel=bool(pygame.mixer.get_init())
        if self.disponivel:
            for nome in ('clique','acerto','erro','vitoria'):
                try:
                    self.efeitos[nome]=pygame.mixer.Sound(str(SOM/f'{nome}.wav'))
                    self.efeitos[nome].set_volume(.55)
                except (pygame.error,OSError):
                    pass
            try:
                pygame.mixer.music.load(str(SOM/'floresta_ambiente.wav'))
                pygame.mixer.music.set_volume(.42 if config['musica'] else 0)
                pygame.mixer.music.play(-1)
            except (pygame.error,OSError):
                pass

    def tocar(self,nome):
        if self.disponivel and self.config['efeitos'] and nome in self.efeitos:
            self.efeitos[nome].play()

    def alternar_musica(self):
        self.config['musica']=not self.config['musica']
        if self.disponivel:
            pygame.mixer.music.set_volume(.42 if self.config['musica'] else 0)

    def alternar_efeitos(self):
        self.config['efeitos']=not self.config['efeitos']


def botao(tela,area,rotulo,fonte,ativo=True):
    apontando=area.collidepoint(pygame.mouse.get_pos())
    cor=VERDE if ativo else CINZA
    if apontando:
        cor=(26,139,104) if ativo else (110,129,118)
    retangulo(tela,area,cor,raio=10)
    texto(tela,fonte,rotulo,area.centerx,area.centery,BRANCO,centro=True)
    return area


def desenhar_teclado(tela,estado):
    regioes=[]
    for i,linha in enumerate(TECLADO):
        espaco=55
        inicio=402-(len(linha)*espaco)//2
        for j,letra in enumerate(linha):
            zona=pygame.Rect(inicio+j*espaco,582+i*57,48,43)
            if letra.lower() in estado['acertadas']:
                cor=VERDE; letra_cor=BRANCO
            elif letra.lower() in estado['erradas']:
                cor=(180,196,174); letra_cor=CINZA
            else:
                cor=CREME; letra_cor=VERDE_PROFUNDO
            if not estado['finalizada'] and zona.collidepoint(pygame.mouse.get_pos()) and letra.lower() not in estado['acertadas']+estado['erradas']:
                cor=(254,228,166)
            retangulo(tela,zona,cor,raio=9)
            retangulo(tela,zona,(149,192,159),borda=1,raio=9)
            texto(tela,FONTES['tecla'],letra,zona.centerx,zona.centery,letra_cor,centro=True)
            regioes.append((zona,letra.lower()))
    return regioes


def desenhar(tela,cenario,estado,config,arte,informacao,confirmar):
    tela.blit(cenario,(0,0))
    # Sombras leves dos painéis.
    retangulo(tela,pygame.Rect(30,115,740,644),(57,105,77),raio=21)
    retangulo(tela,pygame.Rect(792,115,380,644),(57,105,77),raio=21)
    retangulo(tela,pygame.Rect(31,110,738,644),(249,252,244),raio=21)
    retangulo(tela,pygame.Rect(793,110,378,644),(249,252,244),raio=21)
    texto(tela,FONTES['titulo'],'FORCA AMAZÔNICA',37,29,VERDE_PROFUNDO)
    texto(tela,FONTES['pequena'],'96 descobertas sobre peixes, frutas e animais da floresta',39,79,VERDE_PROFUNDO)
    zonas={}
    zonas['novo']=botao(tela,pygame.Rect(1002,37,168,41),'NOVO JOGO (F6)',FONTES['mini'])

    texto(tela,FONTES['secao'],f"RODADA {estado['rodada']}",66,145,VERDE)
    texto(tela,FONTES['pequena'],f"CATEGORIA: {estado['categoria'].upper()}",66,194,CINZA)
    texto(tela,FONTES['mini'],'DICA AMAZÔNICA',66,238,VERDE)
    escrever_linhas(tela,FONTES['pequena'],estado['dica'],66,266,650,VERDE_PROFUNDO,3)
    exibicao=montar_exibicao(estado['palavra'],estado['acertadas'])
    fonte=FONTES['palavra']
    if fonte.size(exibicao)[0]>665:
        fonte=FONTES['secao']
    if fonte.size(exibicao)[0]>665:
        fonte=FONTES['tecla']
    texto(tela,fonte,exibicao,402,389,VERDE_PROFUNDO,centro=True)
    texto(tela,FONTES['pequena'],f"VIDAS: {estado['vidas']} DE {MAX_ERROS}",66,446,VERDE)
    for i in range(MAX_ERROS):
        pygame.draw.circle(tela, VERDE_CLARO if i < estado['vidas'] else (204,214,201),(296+i*35,457),12)
    erradas=', '.join(letra.upper() for letra in estado['erradas']) or 'nenhuma'
    texto(tela,FONTES['pequena'],f'ERRADAS: {erradas}',66,486,CINZA)
    cor=RUBI if estado['finalizada'] and estado['vidas']==0 else VERDE_PROFUNDO
    if confirmar:
        escrever_linhas(tela,FONTES['mini'],'NOVO JOGO? ENTER confirma | ESC cancela',66,523,665,RUBI,2)
    else:
        escrever_linhas(tela,FONTES['mini'],estado['mensagem'],66,523,665,cor,2)
    zonas['letras']=desenhar_teclado(tela,estado)

    texto(tela,FONTES['secao'],'SEU PLACAR',817,147,VERDE)
    # Quatro linhas compactas: o recorde não fica escondido atrás da arte.
    texto(tela,FONTES['placar'],f"Vitórias: {estado['vitorias']}",817,185,VERDE_PROFUNDO)
    texto(tela,FONTES['placar'],f"Pontos: {estado['pontuacao']}",817,210,VERDE_PROFUNDO)
    texto(tela,FONTES['placar'],f"Sequência: {estado.get('sequencia_atual',0)}",817,235,VERDE_PROFUNDO)
    texto(tela,FONTES['placar'],f"Recorde: {estado.get('melhor_sequencia',0)}",817,260,VERDE_PROFUNDO)
    arte.carregar(estado)
    arte.desenhar(tela)
    if estado['finalizada']:
        zonas['proxima']=botao(tela,pygame.Rect(818,658,332,40),'PRÓXIMA RODADA  (ENTER)',FONTES['pequena'])
    zonas['salvar']=botao(tela,pygame.Rect(818,704,104,35),'SALVAR F5',FONTES['mini'])
    zonas['musica']=botao(tela,pygame.Rect(930,704,104,35),'MÚSICA '+('ON' if config['musica'] else 'OFF'),FONTES['mini'],config['musica'])
    zonas['som']=botao(tela,pygame.Rect(1042,704,107,35),'SONS '+('ON' if config['efeitos'] else 'OFF'),FONTES['mini'],config['efeitos'])
    # Rodapé de estado fora dos painéis; não interfere com jogo.
    if estado.get('combo_titulo') and estado['finalizada'] and estado['vidas'] > 0:
        faixa = pygame.Rect(250, 88, 700, 54)
        retangulo(tela, faixa, OURO, raio=18)
        retangulo(tela, faixa, BRANCO, borda=2, raio=18)
        mensagem_combo = estado['combo_titulo']
        if estado.get('sequencia_atual', 0) >= 8:
            mensagem_combo += ' — 8 vitórias seguidas!'
        elif estado.get('sequencia_atual', 0) >= 4:
            mensagem_combo += ' — 4 vitórias seguidas!'
        texto(tela, FONTES['media'], mensagem_combo, faixa.centerx, faixa.centery, VERDE_PROFUNDO, centro=True)
    texto(tela,FONTES['mini'],informacao[:95],37,772,BRANCO)
    pygame.display.flip()
    return zonas


def principal_grafico():
    pygame.mixer.pre_init(22050,-16,1,512)
    pygame.init()
    tela=pygame.display.set_mode((LARGURA,ALTURA))
    pygame.display.set_caption('Forca Amazônica — Edição Deluxe')
    icone=ASSETS/'icone.png'
    if icone.exists():
        try:
            pygame.display.set_icon(pygame.image.load(str(icone)))
        except pygame.error:
            pass
    global FONTES
    FONTES={
        'titulo': pygame.font.SysFont('arial',44,bold=True),
        'secao': pygame.font.SysFont('arial',28,bold=True),
        'palavra': pygame.font.SysFont('consolas',35,bold=True),
        'media': pygame.font.SysFont('arial',25,bold=True),
        'pequena': pygame.font.SysFont('arial',21),
        'placar': pygame.font.SysFont('arial',19),
        'misterio': pygame.font.SysFont('arial',22,bold=True),
        'revelada': pygame.font.SysFont('arial',34,bold=True),
        'revelada_media': pygame.font.SysFont('arial',28,bold=True),
        'revelada_pequena': pygame.font.SysFont('arial',21,bold=True),
        'tecla': pygame.font.SysFont('arial',21,bold=True),
        'mini': pygame.font.SysFont('arial',16),
    }
    cenario=criar_cenario()
    estado,config,informacao=carregar_jogo()
    audio=Audio(config)
    arte=PainelDescoberta()
    clock=pygame.time.Clock()
    confirmar=False
    zonas={}

    def gravar():
        nonlocal informacao
        try:
            destino=salvar_jogo(estado,config)
            informacao=f'Progresso salvo em {destino}'
        except (OSError,ValueError) as erro:
            informacao=f'ERRO AO SALVAR: {erro}'

    def realizar_tentativa(letra):
        resultado=tentar_letra(estado,letra)
        if resultado in ('acerto','erro','vitoria','derrota'):
            audio.tocar('vitoria' if resultado=='vitoria' else 'erro' if resultado in ('erro','derrota') else 'acerto')
            gravar()  # salva a cada letra nova, inclusive a rodada finalizada
        elif resultado in ('repetida','invalida'):
            audio.tocar('clique')

    rodando=True
    while rodando:
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                gravar()
                rodando=False
            elif evento.type==pygame.KEYDOWN:
                if confirmar:
                    if evento.key==pygame.K_RETURN:
                        estado=novo_estado()
                        confirmar=False
                        arte.chave=None
                        gravar()
                    elif evento.key==pygame.K_ESCAPE:
                        confirmar=False
                        informacao='Novo jogo cancelado; seu progresso continua salvo.'
                    continue
                if evento.key==pygame.K_ESCAPE:
                    gravar()
                    rodando=False
                elif evento.key==pygame.K_F5:
                    gravar()
                    audio.tocar('clique')
                elif evento.key==pygame.K_F6:
                    confirmar=True
                    audio.tocar('clique')
                elif evento.key==pygame.K_F8:
                    audio.alternar_musica()
                    gravar()
                elif evento.key==pygame.K_F9:
                    audio.alternar_efeitos()
                    gravar()
                elif evento.key==pygame.K_RETURN and estado['finalizada']:
                    estado=proxima_rodada(estado)
                    gravar()
                elif not estado['finalizada']:
                    realizar_tentativa(evento.unicode)
            elif evento.type==pygame.MOUSEBUTTONDOWN and evento.button==1:
                pos=evento.pos
                if confirmar:
                    continue
                if zonas.get('novo') and zonas['novo'].collidepoint(pos):
                    confirmar=True
                    audio.tocar('clique')
                elif zonas.get('salvar') and zonas['salvar'].collidepoint(pos):
                    gravar()
                    audio.tocar('clique')
                elif zonas.get('musica') and zonas['musica'].collidepoint(pos):
                    audio.alternar_musica()
                    gravar()
                elif zonas.get('som') and zonas['som'].collidepoint(pos):
                    audio.alternar_efeitos()
                    gravar()
                elif estado['finalizada']:
                    if zonas.get('proxima') and zonas['proxima'].collidepoint(pos):
                        estado=proxima_rodada(estado)
                        gravar()
                else:
                    for regiao,letra in zonas.get('letras',[]):
                        if regiao.collidepoint(pos):
                            realizar_tentativa(letra)
                            break
        if rodando:
            zonas=desenhar(tela,cenario,estado,config,arte,informacao,confirmar)
            clock.tick(FPS)
    pygame.quit()


if __name__=='__main__':
    principal_grafico()
