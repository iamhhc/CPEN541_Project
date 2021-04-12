import random
import threading
import time
import tkinter
from tkinter import *
from tkinter import ttk

class EnergyBar:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry("200x200")
        self.progressbar0 = ttk.Progressbar(self.root, orient=VERTICAL, length=100, mode='determinate')
        self.progressbar0.pack(pady=20, padx=5, side=tkinter.LEFT)
        self.progressbar0["value"] = 0

        self.progressbarSum = ttk.Progressbar(self.root, orient=VERTICAL, length=100, mode='determinate')
        self.progressbarSum.pack(pady=20, padx=5,side=tkinter.LEFT)
        self.progressbarSum["value"] = 0

        self.progressbar1 = ttk.Progressbar(self.root, orient=VERTICAL, length=100, mode='determinate')
        self.progressbar1.pack(pady=20, padx=5, side=tkinter.LEFT)
        self.progressbar1["value"] = 0

    def changeBar0Progress(self,value):

        self.progressbar0["value"] = value

    def changeBar1Progress(self, value):
        self.progressbar1["value"] = value

    def changeBarSumProgress(self, value):
        self.progressbarSum["value"] = value



    def start(self,onKeyPress):
        self.root.bind("<KeyPress-a>",onKeyPress)
        self.root.mainloop()


if __name__ == '__main__':
    pass
    # root = tkinter.Tk()
    # progressbar1 = ttk.Progressbar(root, orient=VERTICAL, length=100, mode='determinate')
    # progressbar1.pack(pady=20,padx=5,side=tkinter.LEFT)
    # progressbar1["value"]=50
    # progressbar2 = ttk.Progressbar(root, orient=VERTICAL, length=100, mode='determinate')
    # progressbar2.pack(pady=20,padx=5,side=tkinter.LEFT)
    # progressbar2["value"]=50
    #
    # t1= threading.Thread(target=changeProgress, args=(progressbar1,))
    # t1.start()
    # t2 = threading.Thread(target=changeProgress, args=(progressbar2,))
    # t2.start()


