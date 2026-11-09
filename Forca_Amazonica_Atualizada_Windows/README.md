# Forca Amazônica — Deluxe Textual | Edição Windows

Jogo de forca educativo com **96 palavras** amazônicas (32 peixes, 32 frutas/sementes e 32 outros animais), dicas, 6 vidas, música, efeitos, pontuação, combos e salvamento automático.

**Nesta edição não há fotos nem GIFs de espécies.** Antes de acertar, o painel mostra `?` e **MISTÉRIO AMAZÔNICO**, ambos pulsando e mudando de cor. Após a vitória, o painel revela **a palavra real da rodada** com animação de subida e vibração. Nenhuma imagem de uma espécie é atribuída a outra.

## 1. O que está dentro deste ZIP

- `forca_pygame.py`: jogo gráfico atualizado, somente texto animado.
- `motor_grafico.py`: lógica, pontuação, sequências e salvamento JSON.
- `projeto08_forca.py`: catálogo de 96 palavras e jogo didático em terminal.
- `assets/sons/`: 5 arquivos WAV necessários para música e botões.
- `assets/icone.png` e `assets/icone.ico`: ícone genérico `?`, sem animais.
- `requirements.txt`: pygame-ce.
- `INICIAR_JOGO_WINDOWS.bat`: abre o jogo com Python, instalando pygame-ce se necessário.
- `GERAR_EXE_WINDOWS.bat`: cria o **aplicativo portátil** `ForcaAmazonica.exe` no próprio Windows.
- `testes/test_motor_grafico.py`: testes do motor.
- `GUIA_JOGOS_RENDERIZACAO.md`: explicações técnicas resumidas.

## 2. Executar em outro Windows com Python

1. Extraia o ZIP inteiro; não execute de dentro da visualização do ZIP.
2. Se necessário, instale o Python no site oficial: https://www.python.org/downloads/windows/
3. Clique duas vezes em `INICIAR_JOGO_WINDOWS.bat`.

Ou abra o terminal nessa pasta e execute:

```powershell
python -m pip install --only-binary=:all: pygame-ce
python forca_pygame.py
```

**A extensão Python do VS Code não substitui a biblioteca pygame-ce.** Se houver múltiplos interpretadores, selecione o correto no VS Code (Ctrl+Shift+P > Python: Select Interpreter).

## 3. Gerar o .exe para Windows — dois cliques

1. No computador **Windows** com Python e internet, extraia todo o ZIP.
2. Clique duas vezes em `GERAR_EXE_WINDOWS.bat`.
3. O script cria `.venv`, instala `pygame-ce` e `pyinstaller` e compila o jogo, sons e ícone.
4. O resultado estará em **`dist\ForcaAmazonica.exe`**.
5. Dê dois cliques no EXE e teste. Você pode copiar **apenas esse executável** para outro computador Windows compatível, sem precisar instalar Python no computador que vai usá-lo.

**Importante:** o `.exe` NÃO está pré-compilado neste ZIP, porque a compilação e o teste de programas PyInstaller para Windows exigem executar o processo em Windows. O `.bat` é o gerador do EXE, não o próprio jogo compilado. Ele não é um instalador com assistente de instalação; cria um aplicativo portátil.

Se aparecer erro de `pip`, confira a internet, a versão do Python e execute o BAT pelo prompt para visualizar as mensagens.

## 4. Como funcionam as rodadas

- 6 vidas por rodada; letras erradas consomem 1 vida; letras repetidas não consomem.
- Vitória: 10 + 5 × vidas restantes em pontos.
- 4 vitórias seguidas: **EXCELENTE!**; 8 vitórias seguidas: **INCRÍVEL!**.
- Derrota zera a sequência atual, mas preserva o recorde.
- O painel revela o nome somente quando todas as letras foram descobertas.

## 5. Salvamento e recuperação

O jogo salva a cada tentativa válida, após cada rodada, quando muda o áudio e ao sair. No Windows fica em:

`%APPDATA%\ForcaAmazonica\progresso.json`

O arquivo JSON é persistente, independente da pasta do jogo ou do EXE; a versão nova aceita saves das versões 1 e 2. **Em um computador diferente, o progresso não é transferido automaticamente:** copie o `progresso.json` do antigo computador para a mesma pasta `%APPDATA%\ForcaAmazonica` do novo, com o jogo fechado.

## 6. Teclas

| Ação | Tecla |
|---|---|
| Adivinhar | Letras A-Z, ou clique no teclado virtual |
| Próxima rodada | Enter (após terminar) |
| Salvar | F5 |
| Novo jogo | F6 e Enter para confirmar; Esc cancela |
| Música | F8 |
| Efeitos | F9 |
| Salvar e sair | Esc ou fechar janela |

## 7. Testes

```powershell
python -m unittest discover -s testes -v
```

O conjunto de testes cobre pontuação, tentativa repetida, derrota, continuidade, leitura/gravação, estado inválido e migração de salvamento antigo. A interface precisa ser testada visualmente no Windows. Código construído sem exigência de Pillow, GIFs ou arquivos de imagem de espécies.
