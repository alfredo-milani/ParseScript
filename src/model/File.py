from os.path import isfile


class File(object):
    """
    Classe contente le informazioni necessarie per parsare il file in input
    """

    def __init__(self, file_to_convert_path):
        """

        :param file_to_convert_path: nome del file da convertire

        :type file_to_convert_path: str
        :type extension: str
        :type conversion_algorithm: ConversationAlgorithm
        """
        self.__extension = None
        self.__conversion_algorithm = None
        self.file_to_convert_path = file_to_convert_path

    @property
    def file_to_convert_path(self):
        return self.__file_to_convert_path

    @file_to_convert_path.setter
    def file_to_convert_path(self, value):
        from os.path import islink, isdir
        if not (isdir(value) or islink(value) or isfile(value)):
            raise IOError("Il file: %s non esiste." % value)

        # PyCharm inspection bug
        self.__file_to_convert_path = value
        self.__extension = self.__find_extension()
        self.conversion_algorithm = self.__find_conversion_algorithm()

    @property
    def extension(self):
        return self.__extension

    @extension.setter
    def extension(self, value):
        """
        Setter not available
        """
        raise NotImplementedError

    def __find_extension(self):
        from os.path import splitext
        ext = splitext(self.__file_to_convert_path)[1]

        if not ext:
            return None
        return ext

    def __find_conversion_algorithm(self):
        from control.convertStrategy import TXTAlgorithm, DOCAlgorithm, DOCXAlgorithm, \
            ODTAlgorithm, XLSXAlgorithm, PDFAlgorithm
        from control.convertStrategy import ConversationAlgorithm
        if self.extension == ConversationAlgorithm.EXT_TXT:
            return TXTAlgorithm()
        elif self.extension == ConversationAlgorithm.EXT_DOC:
            return DOCAlgorithm()
        elif self.extension == ConversationAlgorithm.EXT_DOCX:
            return DOCXAlgorithm()
        elif self.extension == ConversationAlgorithm.EXT_ODT:
            return ODTAlgorithm()
        elif self.extension == ConversationAlgorithm.EXT_XLSX:
            return XLSXAlgorithm()
        elif self.extension == ConversationAlgorithm.EXT_PDF:
            return PDFAlgorithm()
        else:
            return None

    @property
    def conversion_algorithm(self):
        return self.__conversion_algorithm

    @conversion_algorithm.setter
    def conversion_algorithm(self, value):
        # PyCharm inspection bug
        from control.convertStrategy import ConversationAlgorithm
        if not isinstance(value, ConversationAlgorithm):
            raise TypeError(
                "Algoritmo di conversione settato in modo errato (estensione del file non supportata)"
            )

        # PyCharm inspection bug
        self.__conversion_algorithm = value

    def get_list_from_file(self):
        """
        Get list of user
        :return: list of @User
        :rtype: list
        """
        return self.conversion_algorithm.convertToList(self.file_to_convert_path)
