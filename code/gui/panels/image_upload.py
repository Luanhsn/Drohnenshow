import tkinter as tk
from tkinter import filedialog

class ImageUploadPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.path = None
        tk.Label(self, text="Bild-Upload (für #image)").pack(anchor="w")
        tk.Button(self, text="Bild auswählen", command=self.upload_image).pack(anchor="w")
        self.status = tk.Label(self, text="Kein Bild ausgewählt")
        self.status.pack(anchor="w")

    def upload_image(self):
        """
        Öffnet einen Dateidialog zur Bildauswahl und speichert den Pfad.
        Aktualisiert die Statusanzeige mit dem ausgewählten Bild.
        """
        path = filedialog.askopenfilename(filetypes=[("Bilder", "*.png;*.jpg;*.jpeg")])
        if path:
            self.path = path
            self.status.config(text=f"Geladen: {path}")

    def get_data(self):
        """
        Gibt den Pfad zum ausgewählten Bild als Dictionary zurück.
        Wird für die spätere Szenenkonfiguration verwendet.
        """
        return {"image_path": self.path}