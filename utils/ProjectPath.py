import os

from utils import Converter


def get_program_folder():
    """
    To get absolute path of the program (path which contain current function's file)
    So this function return the path previous to utils/ProjectPath directory
    :rtype: str
    """
    module_file = __file__
    module_dir = os.path.split(os.path.abspath(module_file))[0]
    program_folder = os.path.abspath(module_dir)
    program_folder_list = program_folder.split(Converter.split_char())
    root_project = Converter.split_char().join(
        x for x in program_folder_list[:len(program_folder_list) - 1]
    )
    return root_project
