from control.convertStrategy import *


class ConverterFactory(object):
    """

    """

    DOC = ".DOC"
    DOCX = ".DOCX"
    ODT = ".ODT"
    PDF = ".PDF"
    TXT = ".TXT"
    XLSX = ".XLSX"

    def __init__(self):
        super(ConverterFactory, self).__init__()

    @classmethod
    def get_converter(cls, converter_type):
        """
        Metodo per ottenere una istanza della classe ConversionAlgorithm

        :param converter_type: estensione del file di cui si vuole ottenere il convertitore;
            da notare che questo parametro DEVE corrispondere ad una delle stringhe dichiarate
            globalmente in classe
        :type converter_type: str

        :return: Classe convertitore
        :rtype: ConversionAlgorithm
        """
        if converter_type is None:
            return None
        elif converter_type.upper() == cls.DOC.upper():
            return DOCAlgorithm.get_instance()
        elif converter_type.upper() == cls.DOCX.upper():
            return DOCXAlgorithm.get_instance()
        elif converter_type.upper() == cls.ODT.upper():
            return ODTAlgorithm.get_instance()
        elif converter_type.upper() == cls.PDF.upper():
            return PDFAlgorithm.get_instance()
        elif converter_type.upper() == cls.TXT.upper():
            return TXTAlgorithm.get_instance()
        elif converter_type.upper() == cls.XLSX.upper():
            return XLSXAlgorithm.get_instance()
        else:
            return None
