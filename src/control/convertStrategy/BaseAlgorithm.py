from constants import *
from control.convertStrategy import Logging
from model import User
from utils import Common


class BaseAlgorithm(object):
    """
    Classe contenente funzioni di uso comune per gli algoritmi di parsing
    """

    def __init__(self):
        super(BaseAlgorithm, self).__init__()
        self.__logs = Logging()

    @property
    def logs(self):
        return self.__logs

    # noinspection PyArgumentList
    def _parse_users_list_v1(self, content):
        """
        Crea una lista di tipo User da @content
        :param content: list
        :return: list
        """
        users_list = []
        i = 0
        while i < len(content):
            # new user found
            if NEW_USER in content[i]:
                name = ""
                surname = ""
                email = ""
                ntel = ""
                scores = []

                i += 1

                # parsing scores
                s = 0
                score_list = [x[0] for x in SCORES_LIST]
                for _ in range(SCORES_NUM):
                    while True:
                        item_position = Common.check_match(content[i], score_list)
                        if item_position != -1 or NEW_USER in content[i]:
                            break
                        i += 1

                    if NEW_USER in content[i]:
                        break

                    i += 1
                    if content[i] != SCORE_VAL_NEGATIVE:
                        if content[i] == SCORE_VAL_POSITIVE:
                            scores.append(SCORES_LIST[item_position][1])
                        else:
                            self.logs.append_logs(
                                Logging.W,
                                "Error parsing value of line: %s.\tValue: %s."
                                "\tPosizione elemento della lista: %d.\n" % (
                                    content[i - 1], content[i], i)
                            )
                            continue

                    i += 1
                    s += 1

                # parsing credentials
                c = 0
                for _ in range(CREDENTIALS_NUM):
                    while True:
                        item_position = Common.check_match(content[i], CREDENTIALS_LIST)
                        if item_position != -1 or NEW_USER in content[i]:
                            break
                        i += 1

                    if NEW_USER in content[i]:
                        break

                    i += 1
                    if CREDENTIALS_LIST[item_position] == CREDENTIAL_NAME:
                        name = content[i]
                    elif CREDENTIALS_LIST[item_position] == CREDENTIAL_SURNAME:
                        surname = content[i]
                    elif CREDENTIALS_LIST[item_position] == CREDENTIAL_EMAIL:
                        email = content[i]
                    elif CREDENTIALS_LIST[item_position] == CREDENTIAL_NTEL:
                        ntel = content[i]

                    i += 1
                    c += 1

                user = User(name, email, surname, ntel, scores)
                users_list.append(user)
                if s != SCORES_NUM or c != CREDENTIALS_NUM:
                    self.logs.append_logs(
                        Logging.W,
                        "WARNING: Error parsing User: " + user + "\n"
                    )

                if NEW_USER in content[i]:
                    continue

            i += 1

        return users_list

    # noinspection PyArgumentList
    def _parse_users_list_v2(self, content):
        """
        Crea una lista di tipo User da @content
        :type content: list
        :rtype: list
        """
        score_list = [x[0] for x in SCORES_LIST]
        users_list = []
        i = 0
        while i < len(content):
            # New user found
            if NEW_USER in content[i]:
                name = ""
                surname = ""
                email = ""
                ntel = ""
                scores = []

                s, c = 0, 0
                while i + 1 < len(content) and NEW_USER not in content[i + 1] and \
                        i + 2 < len(content) and NEW_USER not in content[i + 2]:
                    i += 1
                    item_position = Common.check_match(content[i], score_list)
                    # Item found in scores
                    if item_position != -1:
                        i += 1
                        s += 1
                        if content[i] != SCORE_VAL_NEGATIVE:
                            if content[i] == SCORE_VAL_POSITIVE:
                                scores.append(SCORES_LIST[item_position][1])
                            else:
                                # Per far stampare anche l'utente interessato
                                s -= 1
                                self.logs.append_logs(
                                    Logging.W,
                                    "Error parsing value of line: %s.\tValue: %s."
                                    "\tPosizione elemento della lista: %d." %
                                    (content[i - 1], content[i], i)
                                )

                        continue

                    item_position = Common.check_match(content[i], CREDENTIALS_LIST)
                    # Item found in credentilas
                    if item_position != -1:
                        i += 1
                        c += 1
                        if CREDENTIALS_LIST[item_position] == CREDENTIAL_NAME:
                            name = content[i]
                        elif CREDENTIALS_LIST[item_position] == CREDENTIAL_SURNAME:
                            surname = content[i]
                        elif CREDENTIALS_LIST[item_position] == CREDENTIAL_EMAIL:
                            email = content[i]
                        elif CREDENTIALS_LIST[item_position] == CREDENTIAL_NTEL:
                            ntel = content[i]

                if len(name) != 0 or len(email) != 0 or len(surname) != 0 or len(ntel) != 0 or len(scores) != 0:
                    user = User(name, email, surname, ntel, scores)
                    users_list.append(user)
                    if s != SCORES_NUM or c != CREDENTIALS_NUM:
                        self.logs.append_logs(
                            Logging.W,
                            "WARNING: Error parsing User: " + user + " at position: " +
                            str(i) + " / " + str(i + 1) + "\n"
                        )

            i += 1

        return users_list

    def _parse_users_list(self, content):
        """
        Crea una lista di tipo User da @content
        :type content: list
        :rtype: list
        """
        score_list = [x[0] for x in SCORES_LIST]
        users_list = []
        i = 0
        while i < len(content):
            # New user found
            if NEW_USER in content[i]:
                name = ""
                surname = ""
                email = ""
                ntel = ""
                date = ""
                scores = []

                s, c = 0, 0
                while i + 1 < len(content) and NEW_USER not in content[i + 1]:
                    i += 1
                    item_position = Common.check_match(content[i], score_list)
                    # Item found in scores
                    if item_position != -1:
                        if i + 1 >= len(content) or NEW_USER in content[i + 1]:
                            break
                        elif Common.check_match(content[i + 1], score_list) != -1 or \
                                Common.check_match(content[i + 1], CREDENTIALS_LIST) != -1:
                            self.logs.append_logs(
                                Logging.W,
                                "Unexpected parsing new value even if current is not parsed"
                                "\tPosizione elemento della lista: %d." % i
                            )
                            continue

                        i += 1
                        # Check input values
                        if content[i] != SCORE_VAL_NEGATIVE:
                            if content[i] == SCORE_VAL_POSITIVE:
                                scores.append(SCORES_LIST[item_position][1])
                            else:
                                self.logs.append_logs(
                                    Logging.W,
                                    "Error parsing score value for the line: '%s'.\tValue: '%s'.\t"
                                    "Posizione elemento della lista: %d." %
                                    (content[i - 1], content[i], i)
                                )
                                continue

                        s += 1
                        continue

                    item_position = Common.check_match(content[i], CREDENTIALS_LIST)
                    # Item found in credentials
                    if item_position != -1:
                        if i + 1 >= len(content) or NEW_USER in content[i + 1]:
                            break
                        elif Common.check_match(content[i + 1], score_list) != -1 or \
                                Common.check_match(content[i + 1], CREDENTIALS_LIST) != -1:
                            self.logs.append_logs(
                                Logging.W,
                                "Unexpected parsing new value even if current is not parsed"
                                "\tPosizione elemento della lista: %d." % i
                            )
                            continue

                        i += 1
                        c += 1
                        if CREDENTIALS_LIST[item_position] == CREDENTIAL_NAME:
                            name = content[i]
                        elif CREDENTIALS_LIST[item_position] == CREDENTIAL_SURNAME:
                            surname = content[i]
                        elif CREDENTIALS_LIST[item_position] == CREDENTIAL_EMAIL:
                            email = content[i]
                        elif CREDENTIALS_LIST[item_position] == CREDENTIAL_NTEL:
                            ntel = content[i]
                        elif CREDENTIALS_LIST[item_position] == CREDENTIAL_DATE:
                            date = content[i]

                if name or email or surname or ntel or scores or date:
                    user = User(name, email, surname, ntel, scores, date)
                    users_list.append(user)
                    if s != SCORES_NUM or c != CREDENTIALS_NUM:
                        # Check non effettuato durante l'assegnazione (nel parsing delle credenziali) dal momento che
                        # la funzione filter elimina tutti i valori Falseish
                        # (primary key as in
                        #  https://fs27.formsite.com/lnisrl/form4/fill?1=6536383b0aff580572ef85e25764f3b2)
                        if not (name and email and surname and ntel and date):
                            self.logs.append_logs(
                                Logging.W,
                                "Error parsing credential (name, email, surname, phone number empty or date) "
                                "for User: " +
                                user
                            )
                        elif s == SCORES_NUM:
                            continue

                        self.logs.append_logs(
                            Logging.W,
                            "WARNING: The user may have been converted incorrectly: " + user + "\n"
                        )
                else:
                    self.logs.append_logs(
                        Logging.W,
                        "WARNING: User with all empty entry at position: " + str(i) + " / " + str(i + 1) + "\n"
                    )

            i += 1

        return users_list
