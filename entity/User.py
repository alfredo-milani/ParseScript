# coding=utf-8
class User(object):
    '''
    Classe contente tutte le informazioni necessarie a costituire il file exel

    Attributes:
            name: String che rappresenta il nome dell'utente corrente
            surname: String che rappresenta il cognome dell'utente corrente
            email: String che rappresenta l'indirizzo email dell'utente corrente
            scores: List che contiene le risposte che hanno avuto un esito positivo (cioè 1)
    '''
    def __init__(self, name, email, surname="", ntel="", scores=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.ntel = ntel
        self.scores = scores

    '''
    Per convertire la lista dei punti in stringa
    '''
    def __score_from_list_to_string__(self):
        if self.scores is None or len(self.scores) == 0:
            return "[]"
        return "[" + ", ".join(str(x) for x in self.scores) + "]"

    def __str__(self):
        return self.name + ", " + self.surname + ", " + self.email + ", " + \
               self.ntel + ", " + self.__score_from_list_to_string__()

    # called if: User + "string"
    def __add__(self, other):
        return str(self) + other

    # called if: "string" + User
    def __radd__(self, other):
        return other + str(self)

    '''
    Per convertire l'istanza di User in lista contenente i dati in formato stringa
    '''
    def get_list_from_instance(self):
        return [self.name, self.surname, self.ntel, self.email, self.__score_from_list_to_string__()]
