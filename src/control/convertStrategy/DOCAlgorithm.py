from subprocess import Popen, PIPE

from constants import NEW_USER
from control.convertStrategy.ConversationAlgorithm import ConversationAlgorithm
from control.convertStrategy.BaseAlgorithm import BaseAlgorithm
from utils import Common
from view import ColorsUI


class DOCAlgorithm(ConversationAlgorithm, BaseAlgorithm):
    """
    Classe che definisce l'algoritmo per il parsing di documenti in formato *.doc
    """

    CMD_DOC = "antiword"

    def __init__(self):
        super(DOCAlgorithm, self).__init__()

    def do_convert(self, file_to_convert):
        cmd = [DOCAlgorithm.CMD_DOC, file_to_convert]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        content = stdout.decode(ConversationAlgorithm.DECODE_FORMAT, 'ignore')

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
