import Tkinter
import threading
import time
import ttk

''' Define your Progress Bar function '''


def task(root):
    ft = ttk.Frame()
    ft.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    pb_hD = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')
    pb_hD.pack(expand=True, fill=Tkinter.BOTH, side=Tkinter.TOP)
    pb_hD.start(10)
    root.mainloop()


'''Define the process of unknown duration with root as one of the input And once done, add root.quit() at the end.'''


def process_of_unknown_duration(root=None):
    time.sleep(2)
    print 'Done'
    if root is not None:
        # root.destroy() # distrugge l oggetto
        root.quit() # esce dalla finestra creata (come se si cliccasse quit)


'''
This function will first define root, then call for call for "task(root)" 
--- that's your progressbar, and then call for thread1 simultaneously which will 
execute your process_of_unknown_duration and at the end destroy/quit the root.
'''


if __name__ == '__main__':
    root = Tkinter.Tk()
    t1 = threading.Thread(target=process_of_unknown_duration, args=(root, ))
    t1.start()
    task(root)  # This will block while the mainloop runs
    print "after task(root) finished"
    t1.join()
    print "finished"
