from os import listdir
from os.path import abspath, isfile, isdir

from control.convertStrategy.ConverterFactory import ConverterFactory
from model.BaseFileFactory.File import File
from model.BaseFileFactory.BaseFile import BaseFile
from parsing_exceptions import BadFileExstension
from utils import Common


class Directory(BaseFile):
    """
    Classe che astrae una directory di un file system
    """

    def __init__(self, filename):
        """
        :param is_dir: sempre True
        :param files: contiene solo i files senza considerare le directories
        :param files_with_bad_exstension: files contenuti nella directory con una estensione non supportata
        :param filename: nome della directory

        :type is_dir: bool
        :type files: list
        :type files_with_bad_exstension: list
        :type filename: str
        """
        super(Directory, self).__init__()
        self.__is_dir = True
        self.__files = None
        self.__files_with_bad_exstension = []
        self.filename = filename

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, value):
        if isfile(value):
            from parsing_exceptions import FileException
            raise FileException(value)
        elif not isdir(value):
            from parsing_exceptions import FileNotFound
            raise FileNotFound(value)
        # PyCharm inspection bug
        self.__filename = Common.check_split_char(abspath(value))
        self.__files = self.__get_files()

    @property
    def files_with_bad_exstension(self):
        return self.__files_with_bad_exstension

    @property
    def files(self):
        return self.__files

    @property
    def is_dir(self):
        return self.__is_dir

    def __get_files(self):
        files = []
        for f in listdir(self.filename):
            __file = abspath(self.filename) + Common.split_char() + f
            if isfile(__file):
                try:
                    files.append(File(__file))
                except BadFileExstension:
                    self.__files_with_bad_exstension.append(__file)
                    continue

        return files

    def get_list_from_all_files(self):
        """
        Get list of user from all files in the directory
        :return: list of list of @User
        :rtype: list
        """
        if not self.is_dir:
            from parsing_exceptions import FileException
            raise FileException("Il metodo non puo' essere invocato solo su directory")

        converted_files = []

        for f in self.files:
            converted_files.append(f.get_list_from_file())

        return converted_files
