from model.BaseFileFactory.Directory import Directory
from model.BaseFileFactory.File import File


class BaseFileFactory(object):
    """

    """

    def __init__(self):
        super(BaseFileFactory, self).__init__()

    @staticmethod
    def get_file(filename):
        from os.path import isfile, isdir
        if isfile(filename):
            return File(filename)
        elif isdir(filename):
            return Directory(filename)
        else:
            return None
