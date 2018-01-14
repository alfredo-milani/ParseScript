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


if __name__ == "__main__":
    from utils import Common
    Common.set_up_sys()

    from control import DataRetrievalController
    DataRetrievalController().launch_ui(
        Common.parse_arg(sys.argv[1:])
    )

    # FOR PACKAGING OPERATION UNCOMMENT THIS LINE AND COMMENT ABOVE LINE
    # DataRetrievalController().launch_ui(
    #     parse_arg(["--gui"])
    # )
