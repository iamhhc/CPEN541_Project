
import tkinter as tk
import tkinter as ttk
from tkinter import *
from tkinter import ttk
root = tk.Tk()
frame = tk.Frame(root)
frame.grid()
s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
progressbar0 = ttk.Progressbar(frame, style="red.Horizontal.TProgressbar", orient="horizontal", length=600, mode="determinate", maximum=4, value=1).grid(row=1, column=1)
progressbar1 = ttk.Progressbar(frame, style="red.Horizontal.TProgressbar", orient="vertical", length=100, mode="determinate", maximum=4, value=1).grid(row=2, column=1)
progressbar2 = ttk.Progressbar(frame, style="red.Horizontal.TProgressbar", orient="vertical", length=100, mode="determinate", maximum=4, value=1).grid(row=2, column=2)
frame.pack()


if __name__ == '__main__':
    root.mainloop()