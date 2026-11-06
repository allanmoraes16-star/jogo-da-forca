# Guia de interface, gráficos e renderização de jogos em Python

**Projeto de referência:** Forca Amazônica (Projeto 08 – CETAM)  
**Público:** iniciantes que já conhecem variáveis, condicionais, listas, laços e funções.

## 1. Quatro peças de um jogo

| Parte | Pergunta que responde | Exemplo na Forca |
|---|---|---|
| **Lógica** | O que acontece? | A letra certa revela posições; erro reduz vida |
| **Estado** | Como está o jogo agora? | `vidas`, `pontuacao`, `acertadas`, `rodada` |
| **Interface (UI)** | Como a pessoa interage? | Teclas, botões, textos, placar |
| **Renderização** | Como desenhar tudo na tela? | Fundo, árvore, folhas, letras, atualização da janela |

Uma boa prática é **não colocar `input()` dentro das regras** que a tela gráfica precisa usar. A versão de terminal está separada; a versão opcional gráfica importa as funções `escolher_palavra`, `montar_exibicao` e `venceu`, mas usa eventos do Pygame no lugar do `input()`.

## 2. Mapa visual recomendado

```text
┌────────────────────────────────────────────────────────────────────┐
│  FORCA AMAZÔNICA                                [Como jogar]      │
├───────────────────────────────────────┬────────────────────────────┤
│  RODADA 1                             │  PLACAR                    │
│  DICA: Peixe de escamas...            │  Vitórias: 2               │
│                                       │  Pontos: 75                │
│     t  a  _  _  a  _  _  _             │                            │
│                                       │  ÁRVORE AMAZÔNICA          │
│  Vidas: 5/6  |  Erradas: x           │  5 folhas restantes       │
│  Você acertou a letra A.              │                            │
│                                       │  [Próxima rodada]          │
│    [ Q ][ W ][ E ][ R ][ T ] ...      │                            │
│       [ A ][ S ][ D ] ...             │                            │
└───────────────────────────────────────┴────────────────────────────┘
```

**Prioridade de leitura:** título → dica → palavra → vidas → ação possível → placar. Não faça o jogador procurar a informação essencial.

## 3. Identidade visual amazônica

Uma evolução gráfica coerente pode usar uma floresta estilizada, rios e folhas; não precisa começar com imagens fotográficas.

| Elemento | Cor sugerida | Hexadecimal | Uso |
|---|---|---|---|
| Verde profundo | Verde-escuro | `#003C2D` | Título, textos, contornos |
| Verde vivo | Verde-médio | `#157A55` | Sucesso e botões |
| Verde claro | Menta | `#9FC9B5` | Bordas, fundo de cards |
| Amarelo | Ouro suave | `#FFC857` | Sol, pontuação, elementos em destaque |
| Azul | Azul do rio | `#2F8C9B` | Água, decoração |
| Fundo | Creme claro | `#F6F6E8` | Área de leitura |
| Erro | Vermelho moderado | `#E0645A` | Alertas, usados com ícone ou texto |

**Dica de acessibilidade:** não comunique vitória/erro somente com cor; escreva “Acertou!” e “Errou!”, preserve contraste e use botões com área clicável grande.

## 4. O que é renderização?

Em jogos 2D, renderizar significa **produzir a imagem de cada quadro (frame)**. O Pygame oferece uma `Surface` na qual você desenha; a chamada `pygame.display.flip()` apresenta o frame pronto ao usuário.

```python
import pygame

pygame.init()
tela = pygame.display.set_mode((800, 500))
relogio = pygame.time.Clock()
rodando = True

while rodando:
    # A) Processar entradas do jogador
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # B) Desenhar o frame atual
    tela.fill((246, 246, 232))
    pygame.draw.circle(tela, (255, 200, 87), (660, 90), 45)
    pygame.display.flip()

    # C) Controlar a frequência dos frames
    relogio.tick(60)

pygame.quit()
```

É fundamental **processar a fila de eventos em todo frame**, para receber cliques e comandos de fechar janela; a documentação recomenda isso explicitamente. O `tick(60)` estabelece um limite-alvo de até 60 quadros por segundo, não uma garantia de desempenho.

### Passos para pensar em um frame

1. Capturar eventos (`pygame.event.get()`).
2. Atualizar o estado (`vidas`, `acertadas`, `finalizada`).
3. Limpar ou redesenhar o fundo (`tela.fill`).
4. Desenhar objetos na ordem correta (**camadas**).
5. Exibir a imagem pronta (`pygame.display.flip()`).
6. Controlar o tempo entre frames (`relogio.tick`).

**Camadas:** desenhe primeiro o céu, depois vegetação/rios, depois os painéis da interface, depois texto e botões. O que for desenhado por último aparece por cima.

## 5. Coordenadas, formas e texto

- A origem `(0, 0)` fica no **canto superior esquerdo** da janela; `x` aumenta para a direita e `y` para baixo.
- `pygame.draw.rect(...)` desenha cartões e botões.
- `pygame.draw.circle(...)` desenha sol, frutas e elementos decorativos.
- `pygame.draw.line(...)` desenha galhos, contornos e divisórias.
- `pygame.font.SysFont(...).render(...)` cria uma superfície de texto, que você desenha com `tela.blit(...)`.
- `pygame.Rect` permite verificar se o clique ocorreu **dentro do botão**.

Exemplo básico de botão (desenho **não é automaticamente interativo**):

```python
botao = pygame.Rect(300, 380, 200, 60)
pygame.draw.rect(tela, (21, 122, 85), botao, border_radius=10)

# Dentro da leitura de eventos, para mouse:
if evento.type == pygame.MOUSEBUTTONDOWN:
    if botao.collidepoint(evento.pos):
        print("Botão clicado!")
```

## 6. Melhorando o visual em cinco evoluções

**Etapa 1 — Layout (mais importante):** dimensione fontes; deixe espaços vazios; não coloque dica, placar e palavra na mesma faixa. Use alinhamentos consistentes e textos de alto contraste.

**Etapa 2 — Estados visuais:** teclas ainda não usadas em creme; letras certas em verde; letras erradas em cinza. O usuário entende o jogo sem precisar decorar ações anteriores.

**Etapa 3 — Cenário e feedback:** adicione rio, árvores e um contador de vidas com **seis folhas**. Ao errar, uma folha desaparece. Ao vencer, apresente pontos em texto e destaque a palavra descoberta.

**Etapa 4 — Sprites e animações:** troque formas simples por imagens PNG com transparência para folhas, pássaros e peixes. Crie uma animação curta de folha caindo quando uma vida é perdida. Carregue a imagem uma vez e reaproveite-a no loop. Evite carregar arquivos em todo frame.

**Etapa 5 — Som e telas completas:** acrescente uma tela de abertura, instruções, tela de resultado, efeitos sonoros opcionais e botão para ativar/desativar áudio. Regule volume para não surpreender o jogador.

> Prefira criar sua própria arte ou usar recursos com licenças adequadas, registrando créditos no README. Isso evita problemas ao distribuir o jogo.

## 7. Sprites: exemplo para a próxima aula

```python
# Executado UMA vez na inicialização:
folha = pygame.image.load("assets/folha.png").convert_alpha()
folha = pygame.transform.smoothscale(folha, (48, 48))

# Executado a cada frame (depois de desenhar o cenário):
tela.blit(folha, (850, 350))
```

A função `convert_alpha()` preserva transparência e costuma otimizar o uso da imagem na superfície de exibição. Se ainda não tiver o arquivo `assets/folha.png`, **esse exemplo não roda**; use o desenho de elipse que já funciona no `forca_pygame.py`.

## 8. Tela de jogo: como evitar travamentos

- **Não use `input()` dentro do loop gráfico**: ele interrompe a atualização da janela aguardando texto.
- **Não carregue fonte ou imagem em cada frame**; crie/cache os recursos na inicialização.
- **Processe eventos sempre**, inclusive quando o jogador estiver olhando para a tela de resultado.
- **Limite a taxa de frames** para reduzir o uso desnecessário de CPU.
- **Não misture lógica de vitória com desenho**: a regra deve continuar funcionando mesmo se o visual mudar.
- **Atualize somente o que foi alterado** em sistemas maiores quando fizer sentido; para um jogo pequeno, redesenhar a tela inteira é mais simples.
- **Teste com a tela real**: uma interface bonita em 1100×760 pode não caber num celular. Pygame é muito mais simples em desktop; publicar na web/mobile exige adaptação ou outra tecnologia.

## 9. Do Python ao navegador/celular

O Pygame é excelente para aprender o ciclo de jogos 2D em computadores. Se o objetivo futuro for **um jogo acessível por navegador, inclusive no iPhone e Android**, uma alternativa é implementar a interface em **HTML/CSS/JavaScript** (Canvas 2D), reaproveitando as regras do jogo conceitualmente. Outra opção é estudar motores como **Godot** para projetos de jogo mais avançados. Não é necessário aprender motores 3D para fazer uma forca.

Arquitetura que escala:

```text
regras/        → palavras, verificar letra, pontos
estado/        → rodada atual, vidas, vitórias
interface/     → botões, teclado, telas, textos
assets/        → imagens, fontes licenciadas, sons
entrada/       → teclado, mouse, toque
```

## 10. Minirroteiro de estudo

| Sessão | Tarefa prática | O que observar |
|---|---|---|
| 1 | Executar a versão de terminal | Funções, variáveis, listas |
| 2 | Adicionar uma palavra e rodar testes | Tuplas, módulo `%`, casos-limite |
| 3 | Abrir `forca_pygame.py` e localizar o `while` | Loop de eventos |
| 4 | Mudar cores e posição do placar | Coordenadas, camadas |
| 5 | Criar uma nova folha animada | Sprites e temporização |
| 6 | Testar diferentes resoluções | Layout e acessibilidade |

## 11. Onde estudar depois

- [Documentação oficial do Pygame](https://www.pygame.org/docs/)
- [Janela e atualização da tela — `pygame.display`](https://www.pygame.org/docs/ref/display.html)
- [Eventos — `pygame.event`](https://www.pygame.org/docs/ref/event.html)
- [Fontes e renderização de texto — `pygame.font`](https://www.pygame.org/docs/ref/font.html)
- [Desenho 2D — `pygame.draw`](https://www.pygame.org/docs/ref/draw.html)
- [Imagens — `pygame.image`](https://www.pygame.org/docs/ref/image.html)
- [Relógio e FPS — `pygame.time`](https://www.pygame.org/docs/ref/time.html)

**Meta final:** conseguir explicar em voz alta **qual função guarda os dados, qual função decide o resultado e qual função desenha a tela**. Isso demonstra compreensão da arquitetura, e não apenas capacidade de copiar um programa.
