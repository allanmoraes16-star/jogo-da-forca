@echo off
setlocal
cd /d "%~dp0"
set "PYTHON=python"
where py >nul 2>nul
if not errorlevel 1 set "PYTHON=py -3"
%PYTHON% --version
if errorlevel 1 (
  echo Python nao instalado. Veja o README.
  pause
  exit /b 1
)
%PYTHON% -m pip show pygame-ce >nul 2>nul
if errorlevel 1 (
  echo Instalando pygame-ce para este Python...
  %PYTHON% -m pip install --only-binary=:all: pygame-ce
  if errorlevel 1 (pause & exit /b 1)
)
%PYTHON% forca_pygame.py
if errorlevel 1 pause
