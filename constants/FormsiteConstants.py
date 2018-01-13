# coding=utf-8
"""
Informazioni circa il modello del file da cui estrapolare i dati
"""
NEW_USER = "Scoring Summary"

SCORE_VAL_POSITIVE = '1'
SCORE_VAL_NEGATIVE = '0'
SCORE_AGE = ("1. Hai meno di 18 anni o più di 68?", 1)
SCORE_ALLERGENS = ("2. Sei allergico a frutta secca (noci macadamia, anacardi, noci, mandorle, noci pecan), "
                   "soia, avena, sesamo, o sedano)?", 2)
SCORE_DISTURBANCES = ("3. Ti è stato diagnosticato qualche disturbo cronico o assumi farmaci per un qualsiasi "
                      "disturbo o patologia, come il Diabete (tipo 1 o tipo 2), patologie cardiovascolari, "
                      "renali, epatiche o ha mai avuto episodi di svenimento?", 3)
SCORE_INFECTION = ("4. Hai frequentemente febbre, tosse, diarrea o segni di infezione attiva?", 4)
SCORE_PREGNANT = ("5. Sei incinta o stai allattando?", 5)
SCORE_IMC = ("6. Hai un indice di massa corporea inferiore (IMC) a 18 o maggiore di 40? "
             "Se non conosci il tuo IMC, che è basato su peso e altezza, clicca qui per trovarlo - clicca qui.", 6)
SCORES_LIST = [
    SCORE_AGE,
    SCORE_ALLERGENS,
    SCORE_DISTURBANCES,
    SCORE_INFECTION,
    SCORE_PREGNANT,
    SCORE_IMC
]
SCORES_NUM = len(SCORES_LIST)

# Ridotta la lunghezza del match necessario a soddisfare l'uguaglianza
# a causa di problemi di decodifica con da formato *.docx
# before: "Nome: *"; now: "Nome:"
CREDENTIAL_NAME = "Nome:"
CREDENTIAL_SURNAME = "Cognome:"
CREDENTIAL_EMAIL = "Email:"
CREDENTIAL_NTEL = "Telefono:"
CREDENTIALS_LIST = [
    CREDENTIAL_NAME,
    CREDENTIAL_SURNAME,
    CREDENTIAL_EMAIL,
    CREDENTIAL_NTEL
]
CREDENTIALS_NUM = len(CREDENTIALS_LIST)

HEADER_ROW = [
    "nome",
    "cognome",
    "telefono",
    "email",
    "scores",
    "note"
]

STATUS_SURVEY = "Status"
STATUS_SURVEY_COMPLETE = "Complete"
STATUS_SURVEY_INCOMPLETE = "Incomplete"
