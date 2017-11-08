#!/bin/bash
# ============================================================================
# Titolo:           inst_xlsxwriter.sh
# Descrizione:      Installazione package xlsxwriter
# Autore:           Alfredo Milani (alfredo.milani.94@gmail.com)
# Data:             sab 21 ott 2017, 15.52.00, CEST
# Licenza:          MIT License
# Versione:         0.0.1
# Note:             xlsxwriter: package per manipolare file Exel
# Versione bash:    4.4.12(1)-release
# ============================================================================
declare -r TMP="/dev/shm";
declare -r REL_PATH="utils/packages";



echo "Premi '1' per installare i package 'xlsxwriter' tramite tarball oppure '2' per scaricarlo tramite internet";
read choise;

case ${choise} in
    1 )
        cd ${REL_PATH};
        package_folder_name="XlsxWriter-RELEASE_1.0.2";
        package_name="XlsxWriter-RELEASE_1.0.2.tar.gz";
        ! [ -e ${package_name} ] && echo "Il file $package_name non è stato trovato" && exit 1;
        tar -zxvf XlsxWriter*.tar.gz -C ${TMP};
        cd ${TMP}/${package_folder_name};
        sudo python setup.py install;
        exit 0;
        ;;

    2 )
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
