:: ============================================================================
:: Titolo:           launcher_win.bat
:: Descrizione:      Launcher di DataRetrieval.py con interfaccia grafica
:: Autore:           Alfredo Milani (alfredo.milani.94@gmail.com)
:: Data:             sab 21 ott 2017, 15.52.00, CEST
:: Licenza:          MIT License
:: Versione:         0.9.0
:: Note:             --/--
:: Versione bash:    4.4.12(1)-release
:: ============================================================================
@echo off
set tab=
set tool=..\DataRetrieval.py
set dir_to_convert=..\DATA_TO_CONVERT
set dir_converted=..\DATA_CONVERTED

echo Starting %tool% with GUI
echo Current directory: %cd%

echo.
:: TODO imposta variabile di debug (come in script *.sh)
:: Testa operatore & per eseguire comandi multipli su una singola linea
%tool% --I="%dir_to_convert%" --O=%dir_converted% --not-ask

pause
