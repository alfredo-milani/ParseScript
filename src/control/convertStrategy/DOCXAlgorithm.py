from docx import opendocx, getdocumenttext

from constants import NEW_USER
from control.convertStrategy.BaseAlgorithm import BaseAlgorithm
from control.convertStrategy.ConversionAlgorithm import ConversionAlgorithm
from utils import Common


class DOCXAlgorithm(BaseAlgorithm, ConversionAlgorithm):
    """
    Classe che definisce l'algoritmo per il parsing di documenti in formato *.docx
    """

    def __init__(self):
        super(DOCXAlgorithm, self).__init__()

    def do_convert(self, file_to_convert):
        document = opendocx(file_to_convert)
        paratextlist = getdocumenttext(document)
        newparatextlist = []
        for paratext in paratextlist:
            newparatextlist.append(paratext.encode(ConversionAlgorithm.ENCODE_UTF_8))
        content = '\n\n'.join(newparatextlist)

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
