@echo off
pyinstaller --noconsole --onefile main.py

:: Esperar a que termine la compilación durante 8 segundos
timeout /t 8 >nul

:: Copiar el ejecutable renombrado
copy /Y "dist\main.exe" "key.exe"

:: Limpiar carpetas temporales
rmdir /S /Q build
rmdir /S /Q dist
del /Q *.spec
