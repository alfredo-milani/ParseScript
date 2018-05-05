import threading

from constants import NEW_USER
from control.convertStrategy.BaseAlgorithm import BaseAlgorithm
from control.convertStrategy.ConversionAlgorithm import ConversionAlgorithm

from cStringIO import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
# http://stackoverflow.com/questions/5725278/python-help-using-pdfminer-as-a-library
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from utils import Common
from view import ColorsUI


class PDFAlgorithm(ConversionAlgorithm, BaseAlgorithm):
    """
    Classe che definisce l'algoritmo per il parsing di documenti in formato *.pdf
    """

    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if PDFAlgorithm.__instance is not None:
            from parsing_exceptions import SingletonException
            raise SingletonException(PDFAlgorithm)
        else:
            super(PDFAlgorithm, self).__init__()
            PDFAlgorithm.__instance = self

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    PDFAlgorithm()
        return cls.__instance

    def do_convert(self, file_to_convert):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()
        device = TextConverter(
            rsrcmgr,
            retstr,
            codec=ConversionAlgorithm.ENCODE_UTF_8,
            laparams=laparams
        )

        fp = file(file_to_convert, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pagenos = set()
        for page in PDFPage.get_pages(
                fp,
                pagenos,
                maxpages=0,
                password="",
                caching=True,
                check_extractable=True
        ):
            interpreter.process_page(page)

        try:
            content = retstr.getvalue()
        except IOError:
            return None
        finally:
            fp.close()
            device.close()
            retstr.close()

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
