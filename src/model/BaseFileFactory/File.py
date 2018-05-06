import random

from os.path import isfile, abspath, basename, splitext, isdir

from control.convertStrategy.ConverterFactory import ConverterFactory, ConversionAlgorithm
from model.BaseFileFactory.BaseFile import BaseFile


class File(BaseFile):
    """
    Classe che astrae un file di un file system
    """

    def __init__(self, filename):
        """
        :param extension: estensione del file
        :param conversion_algorithm: istanza dell'algoritmo di conversione
        :param is_dir: sempre False
        :param filename: nome del file
        :param files: istanza corrente

        :type extension: str
        :type conversion_algorithm: ConversionAlgorithm
        :type is_dir: bool
        :type filename: str
        :type files: list
        """
        super(File, self).__init__()
        self.__extension = None
        self.__conversion_algorithm = None
        self.__is_dir = False
        self.filename = filename
        self.__files = self

    @property
    def conversion_algorithm(self):
        return self.__conversion_algorithm

    @conversion_algorithm.setter
    def conversion_algorithm(self, value):
        # PyCharm inspection bug
        from control.convertStrategy import ConversionAlgorithm
        if not isinstance(value, ConversionAlgorithm):
            from parsing_exceptions import BadFileExstension
            raise BadFileExstension(self.filename)

        # PyCharm inspection bug
        self.__conversion_algorithm = value

    @property
    def files(self):
        return [self.__files]

    @property
    def extension(self):
        return self.__extension

    @extension.setter
    def extension(self, value):
        """
        Setter not available
        """
        raise NotImplementedError

    @staticmethod
    def find_extension(file_to_check):
        from os.path import splitext
        ext = splitext(file_to_check)[1]

        if not ext:
            return None
        return ext

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, value):
        if isdir(value):
            from parsing_exceptions import DirectoryException
            raise DirectoryException(value)
        elif not isfile(value):
            from parsing_exceptions import FileNotFound
            raise FileNotFound(value)
        # PyCharm inspection bug
        self.__filename = abspath(value)
        self.__extension = self.find_extension(self.filename)
        self.conversion_algorithm = ConverterFactory().get_converter(self.extension)

    @property
    def is_dir(self):
        return self.__is_dir

    def get_list_from_file(self):
        """
        Metodo per parsare gli utenti contenuti nel file
        :return: lista contenente gli @User parsati dal file
        :rtype: list
        """
        if self.is_dir:
            from parsing_exceptions import DirectoryException
            raise DirectoryException("Il metodo non puo' essere invocato solo su file")

        conversion_algorithm = ConverterFactory().get_converter(
            File.find_extension(self.filename)
        )

        return [] if not conversion_algorithm else conversion_algorithm.convert_to_list(self.filename)

    def get_basename(self):
        """
        Metodo per ottenere il nome base del file
        :return: nome base del file
        :rtype: str
        """
        return basename(self.filename)

    def get_basename_without_exstension(self):
        """
        Metodo per ottenere il nome base del file senza estensione
        :return: nome base del file senza estensione
        :rtype: str
        """
        return splitext(self.get_basename())[0]

    def get_parsed_basename(self):
        """
        Ritorna il nome base del file con estensione *.xlsx
        :return: nome base del file con estensione *.xlsx
        :rtype: str
        """
        return self.get_basename_without_exstension() + ConversionAlgorithm.EXT_XLSX

    def get_new_basename(self):
        """
        Metodo che ritorna un nuovo nome base per il file se ne esiste gia' un altro con lo stesso nome
        :return: nome base del file
        :rtype: str
        """
        # TODO potrebbe ancora esistere un file con lo stesso nome -> genera codice da funzione hash
        return self.get_basename_without_exstension() + "_" + \
               str(random.randint(0, 100000)) + ConversionAlgorithm.EXT_XLSX
