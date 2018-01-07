#!/usr/bin/python
# ============================================================================
# Titolo:           Main.py
# Descrizione:      Script per estrapolare dati da un file *.txt ed inserirli in un file *.xlsx
# Autore:           Alfredo Milani (alfredo.milani.94@gmail.com)
# Data:             ven 20 ott 2017, 19.36.00, CEST
# Licenza:          MIT License
# Versione:         2.0.0
# Note:             --/--
# Versione bash:    4.4.12(1)-release
# ============================================================================
import sys

from control import DataRetrievalController
from utils.Common import set_up_sys, parse_arg

if __name__ == "__main__":
    set_up_sys()

    DataRetrievalController().launch_ui(
        parse_arg(sys.argv[1:])
    )

    # FOR PACKAGING OPERATION UNCOMMENT THIS LINE AND COMMENT ABOVE LINE
    # DataRetrievalController().launch_ui(
    #     parse_arg(["--gui"])
    # )
