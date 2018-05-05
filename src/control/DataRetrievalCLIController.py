from control import DataRetrievalController


class DataRetrievalCLIController(DataRetrievalController):
    """
    Controllore per le view che estendono l'interfaccia in view/DataRetrievalCLI
    """

    def __init__(self):
        super(DataRetrievalCLIController, self).__init__()
