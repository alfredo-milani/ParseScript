#!/usr/bin/python
import sys

import constants
from constants import SystemConstants
from control import DataRetrievalController

# NOTA: Applicazione del patter MVC approssimativa (View e Controller non completamente isolati)
if __name__ == "__main__":
    DataRetrievalController.set_up_sys()

    # Windows system
    if SystemConstants.OS_TYPE == constants.OS_WIN:
        SystemConstants.TMP_PATH = constants.DEFAULT_TMP_WIN
    # Unix system
    elif SystemConstants.OS_TYPE == constants.OS_LINUX:
        SystemConstants.TMP_PATH = constants.DEFAULT_TMP_LINUX

    DataRetrievalController.launch_ui(
        DataRetrievalController.parse_arg(sys.argv[1:])
    )

    # FOR PACKAGING OPERATION UNCOMMENT THIS LINE AND COMMENT ABOVE LINE
    # DataRetrievalController.launch_ui(
    #   DataRetrievalController.parse_arg(["--gui"])
    # )
