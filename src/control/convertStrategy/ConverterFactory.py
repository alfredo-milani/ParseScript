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
        # TODO riutilizza istanze algoritmi di conversione -> mettere hashmap
        # per discriminare logs dei vari files associati
        if converter_type is None:
            return None
        elif converter_type.upper() == cls.DOC.upper():
            return DOCAlgorithm()
        elif converter_type.upper() == cls.DOCX.upper():
            return DOCXAlgorithm()
        elif converter_type.upper() == cls.ODT.upper():
            return ODTAlgorithm()
        elif converter_type.upper() == cls.PDF.upper():
            return PDFAlgorithm()
        elif converter_type.upper() == cls.TXT.upper():
            return TXTAlgorithm()
        elif converter_type.upper() == cls.XLSX.upper():
            return XLSXAlgorithm()
        else:
            return None
