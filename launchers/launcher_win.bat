:: ============================================================================
:: Titolo:           launcher_win.bat
:: Descrizione:      Launcher di DataRetrieval.py con interfaccia grafica
:: Autore:           Alfredo Milani (alfredo.milani.94@gmail.com)
:: Data:             sab 21 ott 2017, 15.52.00, CEST
:: Licenza:          MIT License
:: Versione:         1.0.0
:: Note:             --/--
:: Versione bash:    4.4.12(1)-release
:: ============================================================================
@ECHO OFF;
SET tool = ../DataRetrieval.py;
ECHO Starting %tool % with GUI;
python %tool % --gui;
