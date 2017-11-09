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
debug=1;
dir_to_convert=../DATA_TO_CONVERT;
dir_converted=../DATA_CONVERTED;
tool=../DataRetrieval.py;

if [ ${debug} == 0 ]; then
    echo "Starting $tool with GUI";
    python ${tool} --gui;
else
    echo "Current directory: `pwd`;"
    echo "Directory where check file: $dir_to_convert";
    # echo "Directory where will be send converted files: $dir_converted";
    echo "Directory where will be send converted files: /dev/shm/";

    echo "";
    echo "Files da convertire presenti in $dir_to_convert:";
    for file in ${dir_to_convert}/*; do
        echo -e "\t$file"
    done

    echo -e "Procedere con l'elaborazione? [Yes / No]\t";
    read choise
    echo "";
    if [ "${choise}" == "Yes" ]; then
        for file in ${dir_to_convert}/*; do
            python ${tool} --I="${file}" --O="$dir_converted" --not-ask;
            echo -e "\n\n";
        done
    fi
fi
