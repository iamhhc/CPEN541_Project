import random
import threading
import time
import tkinter
from tkinter import *
from tkinter import ttk


def changeProgress(progressbar: ttk.Progressbar):
    while True:
        newPrograss = progressbar["value"] + random.randint(-10, 10)

        progressbar["value"] = newPrograss if (newPrograss >= 0 and newPrograss <= 100) else progressbar["value"]

        time.sleep(0.1)



if __name__ == '__main__':
    root = tkinter.Tk()
    progressbar1 = ttk.Progressbar(root, orient=VERTICAL, length=100, mode='determinate')
    progressbar1.pack(pady=20,padx=5,side=tkinter.LEFT)
    progressbar1["value"]=50
    progressbar2 = ttk.Progressbar(root, orient=VERTICAL, length=100, mode='determinate')
    progressbar2.pack(pady=20,padx=5,side=tkinter.LEFT)
    progressbar2["value"]=50

    t1= threading.Thread(target=changeProgress, args=(progressbar1,))
    t1.start()
    t2 = threading.Thread(target=changeProgress, args=(progressbar2,))
    t2.start()

    root.mainloop()
