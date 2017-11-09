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
@ECHO OFF
SET tab=
SET tool=..\DataRetrieval.py
SET dir_to_convert=..\DATA_TO_CONVERT
SET dir_converted=..\DATA_CONVERTED

ECHO Starting %tool% with GUI
ECHO Current directory: %cd%
ECHO Directory where check file: %dir_to_convert%
:: ECHO Directory where will be send converted files: %dir_converted%
ECHO Directory where will be send converted files: R:\\

ECHO.
ECHO Files to convert:
:: TODO imposta variabile di debug (come in script *.sh)
:: Testa operatore & per eseguire comandi multipli su una singola linea
for %%file in (%dir_to_convert%\*) do echo %tab%%%file
for %%file in (%dir_to_convert%\*) do %tool% --I="%%file" --O=%dir_converted% --not-ask