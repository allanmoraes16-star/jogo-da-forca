# Guia didático — Interface, renderização e executável

## Separação entre motor e interface

O `motor_grafico.py` só mantém dados e regras: palavra, rodada, acertos, erros, placar, vitórias consecutivas e JSON. Não depende do pygame. O `forca_pygame.py` desenha a tela e captura teclado/mouse.

## Loop do jogo (game loop)

O `while rodando` executa três etapas: processar `pygame.event.get()`, atualizar o estado com as funções de `motor_grafico`, e redesenhar a tela. `pygame.time.Clock().tick(30)` limita a 30 quadros por segundo, importante para notebooks com pouca RAM.

## Mistério e recompensa sem fotos

`PainelDescoberta` calcula o estado bloqueado/desbloqueado pela condição `estado['finalizada'] and estado['vidas'] > 0`. Se bloqueado, desenha círculo e ? coloridos usando seno para variar posição/tamanho/cor; desenha `MISTÉRIO AMAZÔNICO`. Na vitória, mostra o texto `estado['palavra'].upper()` dentro de um cartão e usa uma função easing cúbica para a entrada de baixo para cima. Não depende de JPG/GIF/Pillow.

## Sons

Os `.wav` ficam em `assets/sons` e são acionados pelo `pygame.mixer.Sound` e `pygame.mixer.music`. O Pygame é inicializado por `pygame.init()` e `pygame.mixer.pre_init()`.

## Empacotamento

`GERAR_EXE_WINDOWS.bat` prepara um ambiente virtual e executa PyInstaller `--onefile --windowed`. Os sons são empacotados com `--add-data`. O PyInstaller coloca os recursos dentro do executável e os extrai temporariamente ao iniciar; `BASE = Path(__file__).resolve().parent` funciona no ambiente empacotado. O JSON **não** é escrito nessa pasta temporária: o jogo usa `%APPDATA%`, evitando perder o save ao sair.

## Por que o EXE é criado no Windows?

PyInstaller não produz um executável Windows válido ao ser executado diretamente no Linux. Compile no mesmo sistema operacional de destino, de preferência Windows 10/11 de 64 bits. O resultado é um `.exe` portátil, e não um APK Android.
