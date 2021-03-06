from subprocess import Popen, PIPE

from constants import NEW_USER
from control.convertStrategy.ConversionAlgorithm import ConversionAlgorithm
from control.convertStrategy.BaseAlgorithm import BaseAlgorithm
from utils import Common


class DOCAlgorithm(BaseAlgorithm, ConversionAlgorithm):
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
        content = stdout.decode(ConversionAlgorithm.DECODE_FORMAT, 'ignore')

        data_list = filter(None, content.split("\n"))
        raw_data_num_users = Common.count_occurences(data_list, NEW_USER)

        list_of_users = self._parse_users_list(data_list)

        if raw_data_num_users != len(list_of_users):
            from control.convertStrategy import Logging
            self.logs.append_logs(
                Logging.W,
                "WARNING:\tUser raw data: %d\tUser parsed: %d.\tCheck if some user missing\n" % (
                    raw_data_num_users,
                    len(list_of_users)
                )
            )

        return list_of_users
