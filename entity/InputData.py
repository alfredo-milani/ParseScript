class InputData(object):
    '''
    Classe contenente tutti i parametri neccessari inseriti dall'utente per parsare il file
    '''
    def __init__(self, input_file="", output_dir="", sheet_title="", reduce_ask=False, gui=False):
        self.input_file = input_file
        self.output_dir = output_dir
        self.sheet_title = sheet_title
        self.reduce_ask = reduce_ask
        self.gui = gui
