# coding=utf-8
LINK_TOOL_CONVERTER_DOCX_TXT = "https://document.online-convert.com/convert-to-txt"
DEFAULT_TMP_WIN = "R:\\"
DEFAULT_TMP_LINUX = "/dev/shm/"
INIT_SCRIPT_NAME = "./support/setup_scripts/linux/inst_xlsxwriter.sh"
OS_WIN = "Windows"
OS_LINUX = "Linux"
OS_TYPE = ""
TMP_PATH = ""
APP_ABS_PATH = ""
APP_ABS_RES = ""


APP_NAME = "Form Data Retrieval"
HELP_MSG = "Con questo tool è possibile fare il parsing di file in formato: *.pdf, *.txt, *.xlsx o *.docx.\n" \
           "Si può scegliere di parsare un solo file o di parsare i files contenuti in una specifica directory"
USAGE_MSG = "\n# Description\n" + HELP_MSG + "\n" \
            "\n# Usage\n" \
            "\t./" + APP_ABS_PATH + "Main.py" + " [Options]\n\n" \
            "# Options\n" \
            "\t-i | --I= | --ifile= )\t\tSetting input file\n" \
            "\t-o | --O= | --odir= )\t\tSetting output directory.\n" \
            "\t\t\t\t\tIf not specified, the files will be created in the default " \
                "temp directory ('%s' -> '%s' | '%s' -> '%s')\n" % (
                    OS_WIN,
                    DEFAULT_TMP_WIN,
                    OS_LINUX,
                    DEFAULT_TMP_LINUX
                ) + \
            "\t-t | --T= )\t\t\tSetting sheet title. Default behaviour: based on input filename\n" \
            "\t--not-ask )\t\t\tRiduces user interaction\n" \
            "\t--gui | --GUI )\t\t\tLaunch script in graphical mode\n" \
            "\t-h | -H | --help | --HELP )\tShow this help\n"


EXIT_SUCCESS = 0
EXIT_ERR_ARG = 1
EXIT_ERR_FILE = 2
EXIT_ERR_BAD_CONTENT = 3
EXIT_ERR_PACKAGE_MISSING = 4
