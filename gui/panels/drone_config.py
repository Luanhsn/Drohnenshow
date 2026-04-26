import tkinter as tk

class DroneConfigPanel(tk.Frame):
    def __init__(self, parent, on_first_scene):
        super().__init__(parent)
        self.on_first_scene = on_first_scene

        tk.Label(self, text="Anzahl Drohnen:").pack(anchor="w")
        self.num_var = tk.StringVar(value="20")
        self.num_drones_entry = tk.Entry(self, textvariable=self.num_var)  # Referenz speichern
        self.num_drones_entry.pack(anchor="w")

        # Drohnenmodell-Mapping
        self.model_mapping = {
            "Quadrotor": "quadrotor",
            "racer": "racer",
            "Simple Drone": "simple_drone",
            "Weiße Drone": "white-drone",
            "mini-Drohne": "mini-drone",
            "Blue-Drone":"blue-drone"
        }
        self.reverse_mapping = {v: k for k, v in self.model_mapping.items()}

        tk.Label(self, text="Drohnenmodell:").pack(anchor="w")
        self.model_var = tk.StringVar(value="Quadrotor")
        tk.OptionMenu(self, self.model_var, *self.model_mapping).pack(anchor="w")

        tk.Button(self, text="➕ Erste Szene erstellen", command=self.on_first_scene).pack(pady=10)

    def get_num_drones(self):
        """
        Gibt die vom Benutzer eingegebene Drohnenanzahl zurück.
        Fällt bei ungültiger Eingabe auf Standardwert 20 zurück.
        """
        try:
            value = int(self.num_drones_entry.get())
            return max(1, value)
        except:
            return 20  # oder raise ValueError("Ungültige Eingabe")

    def get_selected_model(self):
        """
        Gibt das aktuell gewählte Drohnenmodell zurück.
        """
        return self.model_mapping[self.model_var.get()]

    def set_selected_model(self, model_key):
        """
        Setzt das ausgewählte Drohnenmodell anhand des internen Keys.
        Übersetzt dazu den Key in das angezeigte Label.
        """
        if model_key in self.reverse_mapping:
            display_label = self.reverse_mapping[model_key]
            self.model_var.set(display_label)

    def set_num_drones(self, value):
        """
        Setzt die Anzahl der Drohnen im Eingabefeld auf den übergebenen Wert.
        """
        self.num_var.set(str(value))

