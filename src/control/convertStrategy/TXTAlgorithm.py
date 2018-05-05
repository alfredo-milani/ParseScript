import threading

from constants import NEW_USER
from control.convertStrategy import ConversionAlgorithm
from control.convertStrategy.BaseAlgorithm import BaseAlgorithm
from utils import Common
from view import ColorsUI


class TXTAlgorithm(ConversionAlgorithm, BaseAlgorithm):
    """
    Classe che definisce l'algoritmo per il parsing di documenti in formato *.txt
    """

    READ_ONLY = "r"
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if TXTAlgorithm.__instance is not None:
            from parsing_exceptions import SingletonException
            raise SingletonException(TXTAlgorithm)
        else:
            super(TXTAlgorithm, self).__init__()
            TXTAlgorithm.__instance = self

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    TXTAlgorithm()
        return cls.__instance

    def do_convert(self, file_to_convert):
        with open(file_to_convert, TXTAlgorithm.READ_ONLY) as f:
            content = f.read()
            data_list = filter(None, content.split("\n"))
            raw_data_num_users = Common.count_occurences(data_list, NEW_USER)

            list_of_users = self._parse_users_list(data_list)

            if raw_data_num_users != len(list_of_users):
                self.view_instance.print_to_user(
                    "WARNING:\tUser raw data: %d\tUser parsed: %d.\tCheck if some user missing\n" % (
                        raw_data_num_users,
                        len(list_of_users)
                    ),
                    ColorsUI.TEXT_COLOR_WARNING
                )

        return list_of_users
