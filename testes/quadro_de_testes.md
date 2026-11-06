# Quadro de testes — Forca Amazônica (96 palavras)

**Integrantes:** _________________________________________

Verificação automática realizada com `python -m unittest discover -s testes -v`.

| Nº | O que foi testado | Resultado esperado | Resultado obtido | OK? |
|---|---|---|---|---|
| 1 | Estrutura do banco | 96 tuplas, 32 por categoria, 6 vidas | Confirmado | Sim |
| 2 | Integridade do banco | Sem palavras repetidas, vazias ou acentuadas | Confirmado | Sim |
| 3 | Alternância das categorias | Peixes → Frutas → Outros animais | Confirmado | Sim |
| 4 | Rodadas iniciais | Tambaqui, cupuaçu, onça | Confirmado | Sim |
| 5 | Rodadas 96, 97 e 98 | Última, depois primeira e segunda palavra | Confirmado | Sim |
| 6 | Rodada inválida `0` | Exceção `ValueError` | Confirmado | Sim |
| 7 | Categoria de palavra desconhecida | Exceção `ValueError` | Confirmado | Sim |
| 8 | Exibição de `tambaqui` com `t` e `a` | `t a _ _ a _ _ _` | Confirmado | Sim |
| 9 | Verificação de vitória incompleta/completa | `False` / `True` | Confirmado | Sim |
| 10 | Digitar `12`, `ab`, `á`, `t`, ` A ` | Rejeitar entradas inválidas e repetida, aceitar `a` | Confirmado | Sim |
| 11 | Vitória sem erros na rodada 1 | `(True, 40)` | Confirmado | Sim |
| 12 | Derrota com seis erros | `(False, 0)` | Confirmado | Sim |
| 13 | Letra errada repetida seguida de vitória | Uma vida perdida, `(True, 35)` | Confirmado | Sim |
| 14 | Encerrar com uma vitória e entrada inválida no menu | Uma rodada, uma vitória, 40 pontos | Confirmado | Sim |
| 15 | Primeira rodada vitória; segunda derrota | Duas rodadas, uma vitória, 40 pontos | Confirmado | Sim |

**Resultado:** 15 testes executados, 15 passaram, nenhuma falha no código de terminal. Código Pygame também passou pela verificação de sintaxe; a interface gráfica deve ser conferida manualmente no computador com Pygame instalado.

## Testes manuais da versão gráfica (preencha após verificar)

| Cenário | Resultado observado | OK? |
|---|---|---|
| Mostrar as três categorias nas primeiras rodadas | __________________ | ____ |
| Dicas longas sem passar por cima da palavra | __________________ | ____ |
| Teclado físico e clique nos botões | __________________ | ____ |
| Perder seis folhas após seis erros | __________________ | ____ |
| Finalizar rodada e começar a seguinte com ENTER | __________________ | ____ |

## Registro de colaboração

| Pessoa | Parte desenvolvida | Como foi verificada |
|---|---|---|
| __________________ | __________________ | __________________ |
| __________________ | __________________ | __________________ |
