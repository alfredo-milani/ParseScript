from abc import abstractmethod


class ColorsUI(object):
    """
    Contract which define color of user interface
    """

    # Attributi di classe
    TEXT_COLOR_DEFAULT = 0
    TEXT_COLOR_WARNING = -2
    TEXT_COLOR_ERROR = -1
    TEXT_COLOR_SUCCESS = 1
    TEXT_COLOR_START_OPERATION = 2

    def __init__(self):
        super(ColorsUI, self).__init__()

    @classmethod
    @abstractmethod
    def get_color_from_code(cls, type_code):
        """
        Get correct color from @color_list based on @type_code.
        In case of errors return @Color (data type based on selected UI)
        :type type_code: int
        :rtype: Any
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_default_color(cls):
        """
        Get default color
        :rtype: Any
        """
        raise NotImplementedError

    @classmethod
    def get_color_from_log_type(cls, message_type):
        from control.convertStrategy import Logging
        if message_type == Logging.E:
            return cls.TEXT_COLOR_ERROR
        elif message_type == Logging.W:
            return cls.TEXT_COLOR_WARNING
        elif message_type == Logging.N:
            return cls.TEXT_COLOR_DEFAULT
        elif message_type == Logging.S:
            return cls.TEXT_COLOR_SUCCESS
        else:
            return cls.TEXT_COLOR_DEFAULT
