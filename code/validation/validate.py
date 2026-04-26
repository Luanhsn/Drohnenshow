from formation import Formation

class Validate:
    """
    Validiert Szenen im Hinblick auf logische Konsistenz,
    z. B. ob genügend Drohnen für Texte vorhanden sind.
    """

    def __init__(self, total_drones):
        self.total_drones = total_drones
        self.errors = {}  # Map: Szenenindex → Fehlermeldung

    def validate_scene(self, idx, scene):
        """
        Validiert eine einzelne Szene anhand der verfügbaren Drohnen.

        Args:
            idx (int): Index der Szene (zur Fehlerspeicherung).
            scene (dict): Die zu prüfende Szene.
        """
        if scene.get("type") == "#text":
            text = scene.get("text", "")
            if not text:
                return  # kein Text, nichts zu prüfen
            required = Formation().total_drones_for_word(text)
            if required > self.total_drones:
                msg = f"❌ Für Text '{text}' brauchst du {required} Drohnen, aber nur {self.total_drones} verfügbar."
                self.errors[idx] = msg

    def validate_all(self, scenes):
        """
        Validiert alle Szenen in einer Liste und speichert ggf. Fehler.

        Args:
            scenes (List[dict]): Liste aller Szenen, die geprüft werden sollen.
        """
        self.errors.clear()
        for idx, scene in enumerate(scenes):
            self.validate_scene(idx, scene)

    def get_errors(self):
        """
        Gibt alle gesammelten Fehler zurück.
        """
        return self.errors
