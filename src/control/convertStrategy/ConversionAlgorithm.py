from abc import abstractmethod

from control.convertStrategy import Logging


class ConversionAlgorithm(object):
    """
    Classe astratta utilizzata per gestire l'esecuzione dell'algoritmo di parsing

    Note sull'eredotarieta' multipla:
    - quando viene istanziata una classe che eredita da molteplici classi, vengono chiamati
        i costruttori delle classi da cui eredita, da sinistra verso destra
    - il costruttore di default invoca i costruttori di tutte le classi da cui eredita (i cosrtuttori
        delle classi ereditate non sono oinvocati da sinistra verso destra)
    - se una classe C eredita da A e B e queste ultime hanno un attributo con lo stesso nome,
        allora in C quell'attributo sara' considerato come un unico oggetto (si avra' una sola referenza),
        quindi se A ha un metodo che modifica quell'oggetto, queste modifiche saranno visibili in B
        e viceversa
    - se una classe C eredita da A e B e queste ultime hanno un metodo con lo stesso nome,
        allora C considerera' solo il metodo della classe che, nella dichiarazione, sara' piu' a sinistra
        (e.g. class C(A, B) -> verra' utilizzato il metodo di A)
    """

    EXT_XLSX = ".xlsx"
    EXT_TXT = ".txt"
    EXT_DOC = ".doc"
    EXT_DOCX = ".docx"
    EXT_ODT = ".odt"
    EXT_PDF = ".pdf"

    ENCODE_UTF_8 = "utf-8"
    DECODE_FORMAT = "utf-8"

    def __init__(self):
        super(ConversionAlgorithm, self).__init__()
        self.list_of_users = None
        self.__logs = Logging()

    @property
    def logs(self):
        return self.__logs

    @property
    def list_of_users(self):
        return self.__list_of_users

    @list_of_users.setter
    def list_of_users(self, value):
        # PyCharm inspection bug
        self.__list_of_users = value

    def convert_to_list(self, file_to_convert):
        """
        DO NOT EDIT this function!
        This function define conversation algorithm.
        :type file_to_convert: str
        :rtype: list
        """
        self.do_before_convert()
        self.list_of_users = self.do_convert(file_to_convert)
        self.do_after_convert()

        return self.list_of_users

    def do_before_convert(self):
        """
        Actions to perform before that conversion algorithm is triggered
        :rtype: None
        """
        pass

    @abstractmethod
    def do_convert(self, file_to_convert):
        """
        Algoritmo per convertire @file_to_convert in una lista di @User
        :param file_to_convert: file from which parse users
        :type file_to_convert: str

        :return: list of users parsed from @file_to_convert
        :rtype: list
        """
        raise NotImplementedError

    def do_after_convert(self):
        """
        Actions to perform after that conversion algorithm is triggered
        :rtype: None
        """
        pass
