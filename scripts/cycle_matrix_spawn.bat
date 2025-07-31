@echo off
setlocal enabledelayedexpansion

REM Ottieni data e ora correnti
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
REM Estrai anno, mese, giorno, ore, minuti e secondi
set year=%datetime:~0,4%
set month=%datetime:~4,2%
set day=%datetime:~6,2%
set hour=%datetime:~8,2%
set minute=%datetime:~10,2%
set second=%datetime:~12,2%
REM Stampa il timestamp
echo Timestamp inizio: %year%-%month%-%day% %hour%:%minute%:%second%


rem Cicla su ogni file nella cartella
for %%I in (D:\scritturaTesiMagistrale\dump\text\*) do (
    echo "Esegui il comando per %%I"
    python matrix_spawn.py %%I
)

REM Ottieni data e ora correnti
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
REM Estrai anno, mese, giorno, ore, minuti e secondi
set year=%datetime:~0,4%
set month=%datetime:~4,2%
set day=%datetime:~6,2%
set hour=%datetime:~8,2%
set minute=%datetime:~10,2%
set second=%datetime:~12,2%
REM Stampa il timestamp
echo Timestamp fine: %year%-%month%-%day% %hour%:%minute%:%second%


endlocal
