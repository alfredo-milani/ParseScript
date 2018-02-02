# coding=utf-8
class User(object):
    """
    Classe contente le informazioni necessarie a costituire il file exel
    """

    def __init__(self, name, email, surname, ntel, scores, date):
        """
        Istanzia un nuovo utente
        :param name: Nome dell'utente corrente
        :param email: Indirizzo email dell'utente corrente
        :param surname: Cognome dell'utente corrente
        :param ntel: Numero di telefono dell'utente corrente
        :param scores: Risposte che hanno avuto un esito positivo (cioè 1)
        :param date: Data nella quale  stato terminato il questionario

        :type name: str
        :type email: str
        :type surname: str
        :type ntel: str
        :type scores: list
        :type date: str
        """
        self.name = name
        self.surname = surname
        self.email = email
        self.ntel = ntel
        self.scores = scores
        self.date = date

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        # PyCharm inspection bug
        self.__name = value

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, value):
        # PyCharm inspection bug
        self.__surname = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        # PyCharm inspection bug
        self.__email = value

    @property
    def ntel(self):
        return self.__ntel

    @ntel.setter
    def ntel(self, value):
        if not value.isdigit():
            # raise ValueError("The phone number can't accept characters!")
            # print "Phone number contains character: %s" % value
            pass

        # PyCharm inspection bug
        self.__ntel = value

    @property
    def scores(self):
        return self.__scores

    @scores.setter
    def scores(self, value):
        # PyCharm inspection bug
        self.__scores = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        # PyCharm inspection bug
        self.__date = value

    def __score_from_list_to_string(self):
        """
        Per convertire la lista dei punti in stringa
        :rtype: str
        """
        if not self.__scores or len(self.__scores) == 0:
            return "[]"

        return "[" + ", ".join(str(x) for x in self.__scores) + "]"

    def get_list_from_instance(self):
        """
        Per convertire l'istanza di User in lista contenente i dati in formato stringa
        :rtype: list
        """
        return [
            self.__date,
            self.__name,
            self.__surname,
            self.__ntel,
            self.__email,
            self.__score_from_list_to_string(),
            self.__get_first_answere()
        ]

    def __get_first_answere(self):
        """
        Ritorna il numero della prima risposta (in formato stringa) effettuata dall'utente
        Se l'utente non ha risposto ad alcuna domanda ritorna il valore -1
        :rtype: str
        """
        try:
            return str(self.__scores[0])
        except IndexError:
            return str()

    def __str__(self):
        return self.__name + ", " + self.__surname + ", " + self.__email + ", " + \
               self.__ntel + ", " + self.__score_from_list_to_string() + ", " + self.__date

    # Called if: User + "string"
    def __add__(self, other):
        return str(self) + other

    # Called if: "string" + User
    def __radd__(self, other):
        return other + str(self)
