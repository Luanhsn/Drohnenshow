import json
from datetime import datetime
from typing import Optional


class ProjectManager:
    def __init__(self):
        self.current_project = None

    def load_project_json(self, path: str) -> dict:
        """
        Lädt eine Projektkonfiguration aus einer JSON-Datei.
        """
        with open(path, "r", encoding="utf-8") as f:
            self.current_project = json.load(f)
        return self.current_project

    def save_project_json(self, data: dict, path: str) -> None:
        """
        Speichert eine Projektkonfiguration in eine JSON-Datei.

        Args:
            data (dict): Projektdaten, die gespeichert werden sollen.
            path (str): Zielpfad für die JSON-Datei.
            """
        data["modified_at"] = datetime.now().isoformat()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        self.current_project = data

    def create_new_scene(self, name: Optional[str] = None) -> dict:
        """
        Erstellt eine neue leere Szene mit optionalem Textnamen.

        Args:
            name (str, optional): Optionaler Szenentitel.

        Returns:
            dict: Die neu erstellte Szene.
        """
        new_scene = {
            "type": "#text",
            "text": name if name else "",
            "duration": 3.0
        }
        if self.current_project:
            self.current_project.setdefault("scenes", []).append(new_scene)
        return new_scene

    def get_scene(self, name: str) -> Optional[dict]:
        """
        Sucht nach einer Szene mit bestimmtem Textinhalt.

        Args:
            name (str): Der Text, nach dem gesucht wird.

        Returns:
            dict | None: Die gefundene Szene oder None, falls nicht vorhanden.
        """
        if not self.current_project or "scenes" not in self.current_project:
            return None
        for scene in self.current_project["scenes"]:
            if scene.get("text") == name:
                return scene
        return None
