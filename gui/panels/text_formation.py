import tkinter as tk

class TextFormationPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Text / Formation:").pack(anchor="w")
        self.input_var = tk.StringVar(value="HELLO")
        tk.Entry(self, textvariable=self.input_var).pack(anchor="w")

    def get_data(self):
        """
        Gibt den eingegebenen Text in Großbuchstaben als Dictionary zurück.
        """
        return {"text": self.input_var.get().strip().upper()}
