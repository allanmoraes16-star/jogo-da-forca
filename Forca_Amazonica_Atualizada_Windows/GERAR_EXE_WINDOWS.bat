@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Forca Amazonica - Gerar executavel para Windows

echo.
echo ========================================================
echo       FORCA AMAZONICA - GERAR EXECUTAVEL WINDOWS
echo ========================================================
echo.
echo O Python precisa estar instalado neste computador.
echo.
set "PYTHON=python"
where py >nul 2>nul
if not errorlevel 1 set "PYTHON=py -3"
%PYTHON% --version
if errorlevel 1 goto :sem_python

echo.
echo [1/3] Preparando ambiente isolado...
if not exist ".venv\Scripts\python.exe" (
  %PYTHON% -m venv .venv
  if errorlevel 1 goto :erro
)

echo.
echo [2/3] Instalando Pygame CE e PyInstaller...
".venv\Scripts\python.exe" -m pip install --only-binary=:all: -r requirements.txt pyinstaller
if errorlevel 1 goto :erro

echo.
echo [3/3] Criando o executavel portatil...
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --onefile --windowed --name ForcaAmazonica --icon "assets\icone.ico" --add-data "assets\sons;assets\sons" --add-data "assets\icone.png;assets" forca_pygame.py
if errorlevel 1 goto :erro

if not exist "dist\ForcaAmazonica.exe" goto :erro
echo.
echo SUCESSO! O executavel foi gerado em:
echo %~dp0dist\ForcaAmazonica.exe
echo.
echo Teste o executavel antes de copiar para outro PC.
start "" "%~dp0dist"
pause
exit /b 0

:sem_python
echo.
echo Python nao encontrado. Instale pelo site oficial:
echo https://www.python.org/downloads/windows/
echo Depois execute este arquivo BAT novamente.
pause
exit /b 1

:erro
echo.
echo Ocorreu uma falha. Leia as mensagens acima.
echo Veja o README para diagnosticar e conferir a versao do Python.
pause
exit /b 1
