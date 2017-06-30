#!/apps/python_3.5/bin/python3
# -*- coding: utf-8 -*-
"""Import inventory from xlsx file.

Uses openpyxl.
"""

import tkinter as tk
from datetime import datetime
from enum import Enum


# Middle imports


from sqlite_engine import session_scope
from models import Item, FIFOItem, Category, ItemCategory


__author__ = 'Brett R. Ward'

# Constants


class App(tk.Frame):
    """Main app."""

    def __init__(self, master=None):
        """Initialze main app."""
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()

    def createWidgets(self):
        """Create widgets in frame."""
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1) 

        self.button_quit = tk.Button(self, text='Quit', command=self.quit)
        self.button_quit.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)


def main():
    """Main program."""
    app = App()
    app.master.title('WoF Management')
    app.mainloop()


if __name__ == "__main__":
    main()
