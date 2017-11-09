#!/bin/bash
# ============================================================================
# Titolo:           setup.sh
# Descrizione:      Installazione package xlsxwriter
# Autore:           Alfredo Milani (alfredo.milani.94@gmail.com)
# Data:             sab 21 ott 2017, 15.52.00, CEST
# Licenza:          MIT License
# Versione:         0.5.0
# Note:             xlsxwriter: package per manipolare file Exel
# Versione bash:    4.4.12(1)-release
# ============================================================================
declare -r TMP="/dev/shm";
declare -r REL_PATH="support/packages";

# TODO da completare con l'installazione degli altri packages

echo "Premi 'OK' per installare il package 'xlsxwriter' tramite internet";
read choise;

case ${choise} in
    [oO][kK] )
        cd ${TMP};
        curl -O -L http://github.com/jmcnamara/XlsxWriter/archive/master.tar.gz;
        tar -zxvf master.tar.gz;
        cd XlsxWriter-master/;
        sudo python setup.py install;
        exit 0;
        ;;

    * )
        echo "Comando non riconosciuto: "${choise};
esac

exit 1;
