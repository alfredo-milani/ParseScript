import platform
from cStringIO import StringIO
from subprocess import Popen, PIPE

from docx import opendocx, getdocumenttext
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
# http://stackoverflow.com/questions/5725278/python-help-using-pdfminer-as-a-library
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

import constants

EXT_XLSX = ".xlsx"
EXT_TXT = ".txt"
CODEC_UTF_8 = "utf-8"
CMD_DOC = "antiword"
EXT_DOC = ".doc"
EXT_DOCX = ".docx"
CMD_ODT = "odt2txt"
EXT_ODT = ".odt"
EXT_PDF = ".pdf"
DECODE_FORMAT = "utf-8"


def split_char():
    os = platform.system()
    if os == constants.OS_WIN:
        return '\\'
    elif os == constants.OS_LINUX:
        return '/'


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = CODEC_UTF_8
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(
            fp,
            pagenos,
            maxpages=maxpages,
            password=password,
            caching=caching,
            check_extractable=True
    ):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


def document_to_text(file_path):
    filename_list = file_path.rsplit(split_char(), 1)
    filename = filename_list[len(filename_list) - 1]

    if filename[-5:] == EXT_XLSX:
        return EXT_XLSX
    elif filename[-4:] == EXT_TXT:
        with open(file_path, "r") as file_to_parse:
            return file_to_parse.read()
    elif filename[-4:] == EXT_DOC:
        cmd = [CMD_DOC, file_path]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode(DECODE_FORMAT, 'ignore')
    elif filename[-5:] == EXT_DOCX:
        document = opendocx(file_path)
        paratextlist = getdocumenttext(document)
        newparatextlist = []
        for paratext in paratextlist:
            newparatextlist.append(paratext.encode(CODEC_UTF_8))
        return '\n\n'.join(newparatextlist)
    elif filename[-4:] == EXT_ODT:
        cmd = [CMD_ODT, file_path]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode(DECODE_FORMAT, 'ignore')
    elif filename[-4:] == EXT_PDF:
        return convert_pdf_to_txt(file_path)
    else:
        return None
