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
@echo off
set debug=-1
set ui_type=1
set abs_path=%~dp0
set tab=
set tool=%abs_path%..\src\Main.py
set dir_to_convert=%abs_path%..\DATA_TO_CONVERT
set dir_converted=%abs_path%..\DATA_CONVERTED

:switch-case-start
	:: Call and mask out invalid call targets
	goto :switch-case-%debug% 2>nul || (
		:: Default case
		echo Comando sconosciuto
	)
	goto :switch-case-end
  
	:switch-case--1
		:switch-case-start
		:: Call and mask out invalid call targets
		goto :switch-case-%ui_type% 2>nul || (
			:: Default case
			echo UI type sconosciuto
		)
		goto :switch-case-end
  
		:switch-case-0
			:: CLI
			echo "Current directory: %cd%"

			echo.
			%tool% --I="%dir_to_convert%" --O="%dir_converted%" --not-ask
			goto :switch-case-end
   
		:switch-case-1
			:: GUI
			echo "Starting %tool% with GUI"

			echo.
			%tool% --gui
			goto :switch-case-end

		:switch-case-end
	goto :switch-case-end

:switch-case-end

pause
