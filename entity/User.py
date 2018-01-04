# coding=utf-8
class User(object):
    """
    Classe contente le informazioni necessarie a costituire il file exel
    """

    def __init__(self, name, email, surname, ntel, scores):
        """
        Istanzia un nuovo utente
        :param name: Nome dell'utente corrente
        :param email: Indirizzo email dell'utente corrente
        :param surname: Cognome dell'utente corrente
        :param ntel: Numero di telefono dell'utente corrente
        :param scores: Risposte che hanno avuto un esito positivo (cioè 1)

        :type name: str
        :type email: str
        :type surname: str
        :type ntel: str
        :type scores: list
        """
        self.name = name
        self.surname = surname
        self.email = email
        self.ntel = ntel
        self.scores = scores

    def __score_from_list_to_string__(self):
        """
        Per convertire la lista dei punti in stringa
        :rtype: str
        """
        if not self.scores or len(self.scores) == 0:
            return "[]"
        return "[" + ", ".join(str(x) for x in self.scores) + "]"

    def __str__(self):
        return self.name + ", " + self.surname + ", " + self.email + ", " + \
               self.ntel + ", " + self.__score_from_list_to_string__()

    # Called if: User + "string"
    def __add__(self, other):
        return str(self) + other

    # Called if: "string" + User
    def __radd__(self, other):
        return other + str(self)

    def get_list_from_instance(self):
        """
        Per convertire l'istanza di User in lista contenente i dati in formato stringa
        :rtype: list
        """
        return [self.name, self.surname, self.ntel, self.email, self.__score_from_list_to_string__()]
