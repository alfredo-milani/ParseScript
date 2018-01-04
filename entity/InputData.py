# coding=utf-8
class InputData(object):
    """
    Classe che incapsula i parametri neccessari inseriti dall'utente per parsare il file
    """

    def __init__(self, input_file, output_dir, sheet_title="", verbose=False, gui=False):
        """
        Istanzia un oggetto che incapsula l'input dell'utente
        :param input_file: Path del file/directory di input
        :param output_dir: Path della directory di output
        :param sheet_title: Nome del foglio
        :param verbose: Livello verbosità operazioni
        :param gui: Tipo interfaccia utente

        :type input_file: str
        :type output_dir: str
        :type sheet_title: str
        :type verbose: bool
        :type gui: bool
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.sheet_title = sheet_title
        self.verbose = verbose
        self.gui = gui
