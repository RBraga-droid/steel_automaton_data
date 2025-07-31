


@echo off
setlocal enabledelayedexpansion

rem Imposta la cartella di origine dei file
set "cartella_origine=D:\scritturaTesiMagistrale\dump\windbg\"

rem Crea la cartella di destinazione se non esiste già
if not exist "%cartella_destinazione%" mkdir "%cartella_destinazione%"

rem Numero massimo di file da spostare alla volta
set "num_file_per_volta=10"

rem Conta i file nella cartella di origine
set "numero_file=0"
for /f %%i in ('dir /b "%cartella_origine%" 2^>nul ^| find /c /v ""') do set "numero_file=%%i"

rem Loop finché ci sono file da spostare
:loop
if %numero_file% leq 0 goto :eof

rem Ottieni i prossimi file da spostare
set "files_da_spostare="
for /f "tokens=1,%num_file_per_volta% delims= " %%f in ('dir /b "%cartella_origine%" 2^>nul') do (
    set "files_da_spostare=!files_da_spostare! "%%f"
    set /a "numero_file-=1"
    if !numero_file! leq 0 goto :sposta_files
)
:sposta_files

rem Sposta i file nella cartella di destinazione
for %%f in (%files_da_spostare%) do (
	echo %%f
    move "%cartella_origine%\%%~f" "%cartella_destinazione%"
)

rem Continua il loop
goto :loop