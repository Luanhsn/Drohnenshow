import tkinter as tk
from tkinter import ttk

class BackgroundPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Hintergrund / Theme:").pack(anchor="w")
        self.theme_var = tk.StringVar(value="#standard")
        ttk.Combobox(self, textvariable=self.theme_var,
                     values=["#standard", "#stars", "#dark"], state="readonly").pack(anchor="w")
