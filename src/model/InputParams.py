# coding=utf-8
class InputParams(object):
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

        """
        NOTE ABOUT PROPERTIES: a property allows you to abstract away internal implementation details 
        (e.g. input_file is the public interface for __input_file). 
        However, if you directly manipulate __input_file yourself, then your interface will not call setter
        during initialization.
        NOTE: _x = private attribute; __x = super-private attribute
        Gli attributi super-privati non sono visibili dalle classi specializzate
        """
        super(InputParams, self).__init__()
        self.input_file = input_file
        self.output_dir = output_dir
        self.sheet_title = sheet_title
        self.verbose = verbose
        self.gui = gui

    @property
    def input_file(self):
        return self.__input_file

    @input_file.setter
    def input_file(self, value):
        # PyCharm inspection bug
        self.__input_file = value

    @property
    def output_dir(self):
        return self.__output_dir

    @output_dir.setter
    def output_dir(self, value):
        # PyCharm inspection bug
        self.__output_dir = value

    @property
    def sheet_title(self):
        return self.__sheet_title

    @sheet_title.setter
    def sheet_title(self, value):
        # PyCharm inspection bug
        self.__sheet_title = value

    @property
    def verbose(self):
        return self.__verbose

    @verbose.setter
    def verbose(self, value):
        # PyCharm inspection bug
        self.__verbose = value

    @property
    def gui(self):
        return self.__gui

    @gui.setter
    def gui(self, value):
        # PyCharm inspection bug
        self.__gui = value
