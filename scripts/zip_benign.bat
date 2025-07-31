@echo off
setlocal enabledelayedexpansion

REM Imposta il percorso della cartella di input
set "cartella_input=D:\scritturaTesiMagistrale\sample_for_input"

REM Imposta il percorso della cartella di output
set "cartella_output=D:\scritturaTesiMagistrale\sample_for_input"

REM Crea la cartella di output se non esiste
if not exist "%cartella_output%" mkdir "%cartella_output%"

REM Imposta la password per gli archivi 7z
set "password=infected"

REM Naviga nella cartella di input
cd "%cartella_input%"

REM Loop attraverso ogni file nella cartella di input
for %%i in (*.*) do (
    REM Crea l'archivio 7z con password
    C:\Programmi\7-Zip\7z.exe a -p%password% "%cartella_output%\%%~ni.7z" "%%i"
)

echo "Archiviazione completata."
pause
