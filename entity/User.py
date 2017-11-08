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
    def __init__(self, name, surname, email, ntel, scores):
        self.name = name
        self.surname = surname
        self.email = email
        self.ntel = ntel
        self.scores = scores
