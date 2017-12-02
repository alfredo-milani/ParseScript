#!/bin/bash
# ============================================================================
# Titolo:           launcher_linux.sh
# Descrizione:      Launcher di DataRetrieval.py con interfaccia grafica
# Autore:           Alfredo Milani (alfredo.milani.94@gmail.com)
# Data:             sab 21 ott 2017, 15.52.00, CEST
# Licenza:          MIT License
# Versione:         1.0.0
# Note:             Per eseguire questo script aprire una shell bash (Ctrl + Alt + T), portarsi nella directory contenente questo file (/dir/../ParseScript/launchers/) con il comando "cd" e digitare: "./launcher_linux.sh"
# Versione bash:    4.4.12(1)-release
# ============================================================================
debug=-1;
dir_to_convert=../DATA_TO_CONVERT;
dir_converted=../DATA_CONVERTED;
tool=../DataRetrieval.py;

case ${debug} in
    -1 )
        # debug level: off
        echo "Current directory: `pwd`";

        echo "";
        python ${tool} --I="${dir_to_convert}" --O="$dir_converted" --not-ask;
        ;;

    1 )
        # debug level: gui test
        echo "Starting $tool with GUI";
        python ${tool} --gui;
        ;;
esac
