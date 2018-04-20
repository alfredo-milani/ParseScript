import platform
from cStringIO import StringIO
from subprocess import Popen, PIPE

from docx import opendocx, getdocumenttext
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
# http://stackoverflow.com/questions/5725278/python-help-using-pdfminer-as-a-library
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


class Converter(object):
    EXT_XLSX = ".xlsx"
    EXT_TXT = ".txt"
    ENCODE_UTF_8 = "utf-8"
    CMD_DOC = "antiword"
    EXT_DOC = ".doc"
    EXT_DOCX = ".docx"
    CMD_ODT = "odt2txt"
    EXT_ODT = ".odt"
    EXT_PDF = ".pdf"
    DECODE_FORMAT = "utf-8"

    @classmethod
    def split_char(cls):
        from constants import SystemConstants
        os = platform.system()
        if os == SystemConstants.OS_WIN:
            return '\\'
        elif os == SystemConstants.OS_LINUX or os == SystemConstants.OS_MACOS:
            return '/'

    @classmethod
    def convert_pdf_to_txt(cls, path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=cls.ENCODE_UTF_8, laparams=laparams)

        fp = file(path, 'rb')
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
            return retstr.getvalue()
        except IOError:
            return None
        finally:
            fp.close()
            device.close()
            retstr.close()

    @classmethod
    def document_to_text(cls, file_path):
        # TODO gestire IO errors
        filename_list = file_path.rsplit(cls.split_char(), 1)
        filename = filename_list[len(filename_list) - 1]

        if filename[-5:] == cls.EXT_XLSX:
            return cls.EXT_XLSX
        elif filename[-4:] == cls.EXT_TXT:
            with open(file_path, "r") as file_to_parse:
                return file_to_parse.read()
        elif filename[-4:] == cls.EXT_DOC:
            cmd = [cls.CMD_DOC, file_path]
            p = Popen(cmd, stdout=PIPE)
            stdout, stderr = p.communicate()
            return stdout.decode(cls.DECODE_FORMAT, 'ignore')
        elif filename[-5:] == cls.EXT_DOCX:
            document = opendocx(file_path)
            paratextlist = getdocumenttext(document)
            newparatextlist = []
            for paratext in paratextlist:
                newparatextlist.append(paratext.encode(cls.ENCODE_UTF_8))
            return '\n\n'.join(newparatextlist)
        elif filename[-4:] == cls.EXT_ODT:
            cmd = [cls.CMD_ODT, file_path]
            p = Popen(cmd, stdout=PIPE)
            stdout, stderr = p.communicate()
            return stdout.decode(cls.DECODE_FORMAT, 'ignore')
        elif filename[-4:] == cls.EXT_PDF:
            return cls.convert_pdf_to_txt(file_path)
        else:
            return None
