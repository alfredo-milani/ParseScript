from control import DataRetrievalController


class DataRetrievalCLIController(DataRetrievalController):
    """
    Controllore per le view che estendono l'interfaccia in view/DataRetrievalCLI
    """

    def __init__(self):
        super(DataRetrievalCLIController, self).__init__()

    def handle_start(self, input_data):
        self._manage_operation(input_data)
