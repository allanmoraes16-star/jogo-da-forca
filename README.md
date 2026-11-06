# 🌿 Forca Amazônica — Projeto 08 (CETAM Python 80h)

**Integrante(s):** _________________________________________  
**Curso:** Linguagem de Programação Python (CETAM, 80 horas)  
**Situação:** banco ampliado para 96 palavras, lógica testada e versão gráfica opcional atualizada  
**Enunciado de referência:** [Projeto 08, repositório da professora](https://github.com/priscilagon/Linguagem_Programacao_Python/tree/main/python-cetam-80h/projetos-integradores/projeto-08-forca-amazonica)

> Este repositório é um **material de estudo/solução de referência**. Antes de entregar como atividade individual ou em dupla, analise as funções, execute os testes, adapte o trabalho e preencha os campos de autoria e colaboração com informações verdadeiras.

## 1. Ideia e objetivo

O jogador descobre **96 palavras amazônicas**: **32 peixes, 32 frutas e sementes e 32 outros animais**. O catálogo anterior tinha somente seis palavras, portanto agora há **16 vezes mais conteúdo**. Em cada rodada, recebe uma dica e começa com **seis vidas**. Uma letra correta é revelada em todas as suas posições; uma letra errada reduz uma vida. Letras repetidas ou inválidas não são aceitas nem retiram vidas. Ao terminar a rodada, é possível começar outra sem perder a pontuação acumulada.

A aprendizagem principal é **separar um programa em funções pequenas, com parâmetros e retornos**. O jogo também exercita **tuplas, listas, strings, `if`, `for`, `while` e operadores lógicos**.

## 2. Estrutura de arquivos

```text
Forca_Amazonica_Projeto08/
├── projeto08_forca.py          # Jogo terminal e catálogo com 96 palavras
├── forca_pygame.py             # Jogo gráfico: categorias + dicas + 96 palavras
├── README.md                   # Este manual, catálogo e explicações
├── GUIA_INTERFACE_RENDERIZACAO.md # Guia para interfaces e desenho de jogos
└── testes/
    ├── test_projeto08_forca.py # 15 testes automáticos (unittest)
    └── quadro_de_testes.md     # Quadro com casos e resultados
```

## 3. Como executar a versão exigida (terminal)

**Requisito:** Python 3, sem instalação de bibliotecas externas.

1. Abra a pasta do projeto no VS Code ou no terminal.
2. Execute:

   ```bash
   python projeto08_forca.py
   ```

   Se o comando `python` não for reconhecido, tente `python3` (Linux/macOS) ou `py` (Windows).
3. Leia a dica e digite uma letra por vez, usando **Enter**.
4. No fim de cada rodada digite `s` (sim) ou `n` (não).

**Atenção:** o aplicativo *GitHub Mobile* serve principalmente para consultar repositórios e colaborar; ele **não executa Python como um interpretador**. Para praticar no Android, use um ambiente de execução Python compatível; para a versão gráfica com Pygame, a opção mais simples é um computador com Python e Pygame instalados.

### Exemplo de uma jogada

```text
=== FORCA AMAZÔNICA ===
=== RODADA 1 ===
Dica: Peixe de escamas, famoso na culinária do Amazonas

Palavra: _ _ _ _ _ _ _ _
Vidas: O O O O O O
Letras erradas: []
Digite uma letra: t
Acertou!

Palavra: t _ _ _ _ _ _ _
Vidas: O O O O O O
Letras erradas: []
Digite uma letra: a
Acertou!
Palavra: t a _ _ a _ _ _
```

Essa é uma **amostra ilustrativa** das mensagens; não representa o jogo inteiro.

## 4. Entenda cada função

| Requisito | Função/dado | Recebe | Devolve ou realiza | Conceito que você pratica |
|---|---|---|---|---|
| RF01 | `PALAVRAS` | — | Tupla contendo 96 tuplas `(palavra, dica)` | Tuplas e pares |
| RF02 | `escolher_palavra(numero_rodada)` | Número 1, 2, 3... | `(palavra, dica)` | Índices e resto da divisão `%` |
| RF03 | `montar_exibicao(palavra, acertadas)` | Texto + lista | Texto como `t a _ _ a _ _ _` | `for`, `if`, listas, `join` |
| RF04 | `venceu(palavra, acertadas)` | Texto + lista | `True` ou `False` | Booleanos, testes de pertencimento |
| RF05 | `ler_letra(tentadas)` | Lista de já tentadas | Uma letra válida | `input`, `strip`, `lower`, `while` |
| RF06 | `jogar_rodada(numero_rodada)` | Número da rodada | `(ganhou, pontos)` | Estado, laços, contagem, retorno duplo |
| RF07 | `principal()` | — | Controla partidas e placar | Repetição de rodadas, acumuladores |

### 4.1. Por que `(rodada - 1) % 96`?

Em Python, a primeira posição de uma sequência é índice `0`, mas o jogador vê **rodada 1**. Por isso subtraímos 1. O operador `%` devolve **o resto** da divisão pelo tamanho do banco, agora 96:

```python
indice = (numero_rodada - 1) % len(PALAVRAS)
```

| Rodada | Expressão | Índice escolhido |
|---|---|---|
| 1 | `(1 - 1) % 96` | 0 — tambaqui |
| 2 | `(2 - 1) % 96` | 1 — cupuaçu (`cupuacu`) |
| 3 | `(3 - 1) % 96` | 2 — onça (`onca`) |
| 96 | `(96 - 1) % 96` | 95 — queixada |
| 97 | `(97 - 1) % 96` | 0 — tambaqui |

### 4.2. Duas listas que mudam durante o jogo

```python
acertadas = []
erradas = []
```

**Tupla**: catálogo de palavras, que não precisa mudar. **Lista**: histórico de letras, que muda durante a rodada.

Por exemplo, com a palavra `tambaqui`, se a lista `acertadas` contiver `['t', 'a']`, a função `montar_exibicao` percorre as oito posições e exibe:

```text
t a _ _ a _ _ _
```

A letra `a` aparece **duas vezes** porque o laço percorre a palavra, não apenas as letras digitadas.

### 4.3. A entrada precisa ser validada

```python
letra = input("Digite uma letra: ").strip().lower()
if len(letra) != 1 or not ("a" <= letra <= "z"):
    print("Digite apenas UMA letra (de a a z).")
```

- `strip()` elimina espaços no começo/fim.
- `lower()` transforma `A` em `a`.
- `len(letra) != 1` rejeita `ab`, `12`, ou texto vazio.
- `"a" <= letra <= "z"` restringe a **uma letra sem acento**. Usar apenas `isalpha()` não restringiria a entrada a `a–z`.
- `letra in tentadas` detecta repetição, sem consumir vida.

### 4.4. Entenda a rodada como um processo

```text
INÍCIO DA RODADA
    ↓
Escolher palavra e dica; iniciar com 6 vidas
    ↓
Exibir palavra escondida, vidas e letras erradas
    ↓
Ler letra (insistir até ser válida e inédita)
    ↓
A letra está na palavra?
    ├── SIM → adicionar a acertadas
    └── NÃO → adicionar a erradas e subtrair 1 vida
    ↓
Todas as letras apareceram?
    ├── SIM → vitória, somar 10 + 5 × vidas
    └── NÃO → ainda há vidas?
                  ├── SIM → voltar a exibir o estado
                  └── NÃO → derrota, 0 pontos
    ↓
Devolver (ganhou, pontos)
```

Observe: a função `jogar_rodada` **não cuida do total geral de pontos**. Ela calcula somente os pontos de uma rodada. A função `principal` soma os resultados de várias rodadas. Isso é **responsabilidade única**.

### 4.5. Duas informações em um retorno

```python
return True, pontos
```

Python agrupa os dois valores em uma tupla. Quem chama pode desempacotar:

```python
ganhou, pontos = jogar_rodada(1)
```

Na derrota, a função retorna `(False, 0)`.

## 5. Como calcular pontos

A fórmula da vitória é **10 + 5 × vidas restantes**. O teto é **40 pontos** (vitória sem errar). A derrota vale **0**.

| Vidas no momento da vitória | Cálculo | Pontos |
|---|---|---|
| 6 | 10 + 5 × 6 | 40 |
| 5 | 10 + 5 × 5 | 35 |
| 3 | 10 + 5 × 3 | 25 |
| 1 | 10 + 5 × 1 | 15 |
| 0 | Derrota | 0 |

## 6. Como executar os testes

Na pasta principal, execute:

```bash
python -m unittest discover -s testes -v
```

Foram executados **15 testes automáticos com sucesso** no código principal, usando a biblioteca `unittest`. Eles exercitam as regras, inclusive entradas inválidas e casos de borda.

O arquivo `testes/quadro_de_testes.md` traz o quadro de testes solicitado pela atividade, com entradas, esperado e observado. **Os testes da versão gráfica não foram executados neste ambiente**, pois a biblioteca Pygame não está instalada aqui.

## 7. Evolução opcional para gráficos

O arquivo `forca_pygame.py` implementa uma **segunda interface jogável**, que chama funções já existentes do programa principal e utiliza o pacote Pygame.

Instale em um computador:

```bash
python -m pip install --only-binary=:all: pygame-ce
python forca_pygame.py
```

**Controles:** digitar letras no teclado ou clicar nas letras desenhadas; `Enter` para começar outra rodada após vencer/perder; `Esc` para sair. A categoria da palavra é mostrada acima da dica. A árvore amazônica tem **seis folhas**, uma por vida; a cada erro desaparece uma folha. O placar permanece entre rodadas.

A interface é **um exercício extra, não um requisito do CETAM**. Ela serve para experimentar eventos, superfícies, desenhos, fontes, coordenadas e atualização de frames. Consulte `GUIA_INTERFACE_RENDERIZACAO.md` para aprender os conceitos e descobrir como refinar o visual.

## 8. Mapeamento dos critérios de avaliação

| Critério | Onde verificar |
|---|---|
| Funcionamento / placar | `jogar_rodada`, `principal`, testes de vitória/derrota e acumulação |
| Modularização | Funções RF02–RF07; `PALAVRAS` no começo do arquivo |
| Strings e listas | `montar_exibicao`, `ler_letra` e listas `acertadas`/`erradas` |
| Regras RN01–RN06 | Constante `MAX_ERROS`, validação, repetição, fórmula, exibição e placar final |
| Organização/testes | Docstrings, `if __name__ == '__main__'`, `unittest`, quadro de testes |
| Colaboração | Preencher esta seção e o quadro de testes; **não inventar** colaboração |

## 9. Registro de colaboração (preenchimento obrigatório se em dupla)

| Função/atividade | Responsável | O que foi feito |
|---|---|---|
| `PALAVRAS`, `escolher_palavra` | __________________ | __________________ |
| `montar_exibicao`, `venceu` | __________________ | __________________ |
| `ler_letra` | __________________ | __________________ |
| `jogar_rodada` | __________________ | __________________ |
| `principal` | __________________ | __________________ |
| Testes, revisão e README | __________________ | __________________ |

## 10. Desafios para praticar sem copiar

1. **Modifique a dica** de `cupuacu` e acrescente uma nova palavra ao catálogo. O que muda na fórmula da rodada 97?
2. **Reescreva `venceu`** usando `all(...)`. Compare as duas soluções e explique qual você entende melhor.
3. **Adicione uma opção de ajuda** que mostre novamente as regras, sem alterar o placar.
4. **Crie um desenho ASCII** de sete estágios (0 a 6 erros) no terminal.
5. **Troque a escolha sequencial por sorteio** com `random.choice`, sem perder a possibilidade de repetir partidas.
6. **Experimente salvar um recorde** em `placar.txt` e aprenda `with open(...)`.
7. **Execute o teste de rodada 97**, depois acrescente palavras e verifique como `len(PALAVRAS)` altera o ciclo.

### Uma pergunta importante para revisar

**Por que a lista `tentadas` é calculada como `acertadas + erradas`?** Porque o jogador não pode repetir nem uma letra que acertou nem uma que errou. A concatenação reúne os dois históricos para a função de validação, sem alterar as listas originais.

## 11. O novo banco de palavras: 96 termos

| Categoria | Quantidade | Exemplos |
|---|---:|---|
| Peixes amazônicos | 32 | Tambaqui, pirarucu, jaraqui, matrinxã, pirapitinga, bodó, dourada, acará |
| Frutas e sementes | 32 | Cupuaçu, tucumã, açaí, camu-camu, castanha, cubiu, pupunha, uxi |
| Outros animais amazônicos | 32 | Onça, ariranha, boto, peixe-boi, uacari, harpia, jacamim, tracajá |
| **Total** | **96** | **16 vezes o catálogo original** |

### Como o código organiza o catálogo

O programa conserva o requisito do CETAM: **`PALAVRAS` é uma tupla de tuplas `(palavra, dica)`**. Para organizar o conteúdo, mantemos três tuplas adicionais: `PEIXES`, `FRUTAS` e `ANIMAIS`. Este trecho intercala uma palavra de cada categoria:

```python
PALAVRAS = tuple(item for trio in zip(PEIXES, FRUTAS, ANIMAIS) for item in trio)
```

* `zip(...)` agrupa um item de cada categoria;
* `for trio in ...` percorre esses grupos;
* `for item in trio` pega cada par `(palavra, dica)`;
* `tuple(...)` cria o catálogo final imutável.

Assim, as rodadas alternam entre **peixe → fruta/semente → outro animal**, sem repetir palavras até completar 96 rodadas. A rodada 97 volta ao início, como exige o comportamento cíclico do projeto. Essa ordem é determinística (não é sorteio aleatório).

### Como adicionar uma palavra

Dentro da tupla da categoria correta, acrescente outro par:

```python
("nome", "Dica curta, clara e que não entregue a resposta."),
```

A resposta deve conter **somente letras minúsculas de a a z**. Assim: `tucuma` no lugar de `tucumã`, `aracaboi` no lugar de `araçá-boi` e `macacoaranha` no lugar de `macaco-aranha`. A dica, por outro lado, **pode ter acentos e pontuação**.

**Importante ao ampliar novamente:** como usamos `zip`, o agrupamento final pára quando termina a menor das três categorias. Para não perder termos, mantenha as três tuplas com a mesma quantidade de itens, ou adapte a intercalação. Os testes verificam essa contagem.

### Referências para pesquisar novos nomes

- [Embrapa — Fruteiras da Amazônia](https://www.infoteca.cnptia.embrapa.br/infoteca/handle/doc/664664) (nomes de dezenas de frutos regionais).
- [Embrapa — Calendário de fruteiras na Amazônia](https://www.embrapa.br/busca-de-publicacoes/-/publicacao/1122621/calendario-de-fruteiras-na-amazonia-nativas-e-exoticas) (distingue plantas nativas de exóticas).
- [Águas Amazônicas — Peixes prioritários](https://pt.aguasamazonicas.org/pescarias/peixes-prioritarios).
- [ICMBio — Fauna e Flora](https://www.gov.br/icmbio/pt-br/assuntos/biodiversidade/unidade-de-conservacao/unidades-de-biomas/amazonia/lista-de-ucs/parna-da-serra-do-divisor/novo-layout/fauna-e-flora/).

Alguns nomes são populares e abrangem mais de uma espécie. As dicas são descrições educativas simplificadas, não uma chave de identificação zoológica. O banco inclui espécies e grupos que ocorrem na Amazônia; isso não significa que sejam exclusivos dela.

## 12. Próximos passos

A sequência pedagógica recomendada é: **terminal → testes → estrutura de dados → loop de eventos Pygame → sprites e animações → áudio e interface responsiva**. Não é necessário aprender tudo antes de dominar a primeira versão.

**Documentação:** [Python `unittest`](https://docs.python.org/3/library/unittest.html) · [Pygame](https://www.pygame.org/docs/) · [Enunciado original](https://github.com/priscilagon/Linguagem_Programacao_Python/tree/main/python-cetam-80h/projetos-integradores/projeto-08-forca-amazonica).
