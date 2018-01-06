#!/bin/bash
# ============================================================================
# Titolo:           launcher_linux.sh
# Descrizione:      Launcher di DataRetrieval.py con interfaccia grafica
# Autore:           Alfredo Milani (alfredo.milani.94@gmail.com)
# Data:             sab 21 ott 2017, 15.52.00, CEST
# Licenza:          MIT License
# Versione:         2.0.0
# Note:             Per eseguire questo script aprire una shell bash (Ctrl + Alt + T) ed eseguire il file "/path/to/script/launcher_linux.sh"
# Versione bash:    4.4.12(1)-release
# ============================================================================
debug=-1
ui_type=1
abs_path=`dirname $0`
dir_to_convert=${abs_path}/../DATA_TO_CONVERT
dir_converted=${abs_path}/../DATA_CONVERTED
tool=${abs_path}/../Main.py
null=/dev/null

case ${debug} in
    -1 )
        # debug level: off
        case ${ui_type} in
            0 )
                # CLI
                echo "Current directory: `pwd`"

                echo ""
                ${tool} --I="${dir_to_convert}" --O="${dir_converted}" --not-ask
                ;;

            1 )
                # GUI
                echo "Starting $tool with GUI"

                echo ""
                ${tool} --gui &> ${null}
                ;;
        esac
        ;;
esac
