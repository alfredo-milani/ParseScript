import tkFileDialog

from tkinter import *

from DataRetrieval import perform_operation

BUTTON_IN_ID = 1
BUTTON_OUT_ID = 2
TEXT_VIEW_ID = 3


class Redir(object):
    # This is what we're using for the redirect, it needs a text box
    def __init__(self, textbox):
        self.textbox = textbox
        self.textbox.config(state=NORMAL)
        self.fileno = sys.stdout.fileno

    def write(self, message):
        # When you set this up as redirect it needs a write method as the
        # stdin/out will be looking to write to somewhere!
        self.textbox.insert(END, str(message))


def askopenfilename():
    """ Prints the selected files name """
    # get filename, this is the bit that opens up the dialog box this will
    # return a string of the file name you have clicked on.
    filename = tkFileDialog.askopenfilename()
    if filename:
        # Will print the file name to the text box
        print filename


def fetch(entries):
    for entry in entries:
        field = entry[0]
        text = entry[1].get()
        print('%s: "%s"' % (field, text))


def on_click(out):
    # Set up the redirect
    stdre = Redir(out)
    # Redirect stdout, stdout is where the standard messages are output
    sys.stdout = stdre
    # Redirect stderr, stderr is where the errors are printed too!
    sys.stderr = stdre

    askopenfilename()


def start_processing(files_in, out):
    # Set up the redirect
    stdre = Redir(out)
    # Redirect stdout, stdout is where the standard messages are output
    sys.stdout = stdre
    # Redirect stderr, stderr is where the errors are printed too!
    sys.stderr = stdre

    input_file = files_in[0][1].get()
    output_dir = files_in[1][1].get()

    perform_operation(input_file, output_dir, sheet_title="")


def makeform(root):
    entries = []

    row = Frame(root)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    # button = Button(root, text=field, command=askopenfilename)
    button = Button(root, text="Input")
    ent = Entry(row)
    button.bind("<Button-1>", lambda event, out=ent: on_click(out))
    button.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    entries.append(("Input", ent))

    row = Frame(root)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    # button = Button(root, text=field, command=askopenfilename)
    button = Button(root, text="Output directory")
    ent = Entry(row)
    button.bind("<Button-1>", lambda event, out=ent: on_click(ent))
    button.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    entries.append(("Output directory", ent))

    return entries


def init():
    root = Tk()

    ents = makeform(root)

    b1 = Button(root, text='Start')
    b1.pack(side=LEFT, padx=5, pady=5)
    b2 = Button(root, text='Quit', command=root.quit)
    b2.pack(side=RIGHT, padx=7, pady=7)

    # Make a scroll bar so we can follow the text if it goes off a single box
    scrollbar = Scrollbar(root, orient=VERTICAL)
    # This puts the scrollbar on the right handside
    scrollbar.pack(side=RIGHT, expand=NO, fill=Y)
    # Make a text box to hold the text
    textbox = Text(
        root,
        font=("Helvetica", 8),
        state=DISABLED,
        yscrollcommand=scrollbar.set,
        wrap=WORD
    )
    # This puts the text box on the left hand side
    textbox.pack(side=BOTTOM, expand=YES, fill=BOTH)

    # Configure the scroll bar to stroll with the text box!
    scrollbar.config(command=textbox.yview)

    b1.bind("<Button-1>", lambda event, files_in=ents, out=textbox: start_processing(files_in, out))

    root.mainloop()


if __name__ == '__main__':
    init()
