import threading


class ParseThread(threading.Thread):
    """

    """

    __lock = threading.Lock()

    def __init__(self, target, target_args=(), callback=None, callback_args=(), *args, **kwargs):
        super(ParseThread, self).__init__(target=self.__target_with_callback, *args, **kwargs)
        self.__method = target
        self.__method_args = target_args
        self.__callback = callback
        self.__callback_args = callback_args

    def __target_with_callback(self):
        self.__method(*self.__method_args)
        if self.__callback is not None:
            with ParseThread.__lock:
                self.__callback(*self.__callback_args)

    @classmethod
    def get_lock(cls):
        cls.__lock.acquire()

    @classmethod
    def release_lock(cls):
        cls.__lock.release()
