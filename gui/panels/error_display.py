import tkinter as tk

class ErrorDisplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = tk.Label(self, text="", fg="red")
        self.label.pack()

    def show_error(self, text):
        """
        Zeigt die übergebene Fehlermeldung im Label an.
        """
        self.label.config(text=text)

    def clear(self):
        """
        Löscht die aktuell angezeigte Fehlermeldung.
        """
        self.label.config(text="")
