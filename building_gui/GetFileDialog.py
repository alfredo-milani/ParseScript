import tkFileDialog
from Tkinter import *


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


def laucher():
    # Make the root window
    root = Tk()

    # Make a button to get the file name
    # The method the button executes is the askopenfilename from above
    # You don't use askopenfilename() because you only want to bind the button
    # to the function, then the button calls the function.
    button = Button(root, text='GetFileName', command=askopenfilename)
    # this puts the button at the top in the middle
    button.grid(row=1, column=0)

    # Make a scroll bar so we can follow the text if it goes off a single box
    scrollbar = Scrollbar(root, orient=VERTICAL)
    # This puts the scrollbar on the right handside
    scrollbar.grid(row=2, column=3, sticky=N+S+E)

    # Make a text box to hold the text
    textbox = Text(root,font=("Helvetica",8),state=DISABLED, yscrollcommand=scrollbar.set, wrap=WORD)
    # This puts the text box on the left hand side
    textbox.grid(row=2, column=0, columnspan=3, sticky=N+S+W+E)

    # Configure the scroll bar to stroll with the text box!
    scrollbar.config(command=textbox.yview)

    #Set up the redirect
    stdre = Redir(textbox)
    # Redirect stdout, stdout is where the standard messages are output
    sys.stdout = stdre
    # Redirect stderr, stderr is where the errors are printed too!
    sys.stderr = stdre
    # Print hello so we can see the redirect is working!
    print "hello"
    # Start the application mainloop
    root.mainloop()


if __name__ == '__main__':
    laucher()
