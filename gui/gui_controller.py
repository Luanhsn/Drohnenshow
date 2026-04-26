import tkinter as tk
import os
from tkinter import ttk, simpledialog
from formation import Formation
from gui.scene_configurator import SceneConfiguratorPanel
from gui.panels.background import BackgroundPanel
from gui.panels.drone_config import DroneConfigPanel
from gui.panels.error_display import ErrorDisplay
from simulation import run_simulation
from validation.validate import Validate
from tkinter import messagebox, filedialog
from project_manager import ProjectManager

project_manager = ProjectManager()
PROJECTS_DIR = "saved_projects"


class GUIController(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SkyOrchestrator")
        self.geometry("1000x600")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Tab 1: Konfiguration (nur globale Einstellungen)
        self.config_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.config_tab, text="Konfiguration")

        # Panels im Konfig-Tab (global gültig für alle Szenen)
        self.background_panel = BackgroundPanel(self.config_tab)
        self.background_panel.pack(pady=5)

        self.drone_config = DroneConfigPanel(self.config_tab, self.create_first_scene)
        self.drone_config.pack(pady=10)

        self.error_display = ErrorDisplay(self.config_tab)
        self.error_display.pack(pady=10)

        self.start_button = tk.Button(self, text="🚀 Simulation starten", command=self.on_simulation_start,
                                      font=("Arial", 12, "bold"), bg="green", fg="white")
        self.start_button.pack(pady=10)

        self.scene_tab = None

        self.sidebar = tk.Frame(self, width=250, bg="#eee")
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="Projekte", bg="#eee", font=("Arial", 12, "bold")).pack(pady=10)
        self.project_listbox = tk.Listbox(self.sidebar)
        self.project_listbox.pack(fill="y", expand=True, padx=10)
        self.project_listbox.bind("<<ListboxSelect>>", self.on_project_select)

        self.protocol("WM_DELETE_WINDOW", self.ask_to_save_before_exit)

        self.refresh_project_list()

        tk.Button(self.sidebar, text="+ Neues Projekt", command=self.new_project_dialog).pack(pady=10)

        self.project_listbox.bind("<<ListboxSelect>>", self.on_project_select)

        tk.Button(self.sidebar, text="+ Neues Projekt", command=self.new_project_dialog).pack(pady=10)

        self.current_project_path = None

        btn_frame = tk.Frame(self)
        btn_frame.pack(anchor="ne", padx=10, pady=5)

        tk.Button(btn_frame, text="💾 Speichern", command=self.save_project).pack(side="left", padx=5)
        tk.Button(btn_frame, text="📤 Exportieren", command=self.export_project).pack(side="left", padx=5)

        self.project_label = tk.Label(self, text="🔄 Kein Projekt geladen", font=("Arial", 10, "italic"))
        self.project_label.pack(anchor="ne", padx=10, pady=5)

    def create_first_scene(self):
        """
        Erstellt den ersten Szenen-Tab, wenn noch keiner existiert,
        und aktiviert ihn im Notebook.
        """
        if not self.scene_tab:
            self.scene_tab = SceneConfiguratorPanel(self.notebook, auto_first_scene=False)
            self.notebook.add(self.scene_tab, text="Szenen")
            self.notebook.select(self.scene_tab)

    def run(self):
        """
        Startet die Haupt-GUI-Schleife.
        """
        self.mainloop()

    def on_simulation_start(self):
        """
        Führt Validierung durch und startet die Simulation mit der aktuellen Konfiguration.
        Zeigt Fehler an, wenn Konfiguration unvollständig oder ungültig ist.
        """
        if not self.scene_tab:
            self.error_display.show_error("Bitte erst mindestens eine Szene erstellen.")
            return

        # Drohnenanzahl aktualisieren aus dem Entry-Feld
        try:
            entered = self.drone_config.get_num_drones()
            self.scene_tab.global_config["num_drones"] = entered
        except:
            self.error_display.show_error("Ungültige Drohnenanzahl.")
            return

        self.scene_tab.global_config["bg-theme"] = self.background_panel.theme_var.get()
        self.scene_tab.global_config["drone-model"] = self.drone_config.get_selected_model()

        config = self.scene_tab.get_full_config()

        if not config["scenes"]:
            self.error_display.show_error("Keine Szenen definiert.")
            return

        if config["num_drones"] <= 0:
            self.error_display.show_error("Ungültige Drohnenanzahl.")
            return

        self.error_display.clear()  # global leeren

        formation = Formation()
        has_scene_error = False
        scene_errors = []

        # Fehler pro Szene prüfen
        for idx, scene in enumerate(config["scenes"]):
            scene["num_drones"] = config["num_drones"]  # sicherheitshalber

            if scene.get("type") == "#text":
                required = formation.total_drones_for_word(scene["text"])
                available = config["num_drones"]
                if required > available:
                    has_scene_error = True
                    msg = f"❌ Für Text '{scene['text']}' brauchst du {required} Drohnen, aber nur {available} verfügbar."
                    scene_errors.append(msg)

                    try:
                        frame = self.scene_tab.scene_tabs[idx]
                        if hasattr(frame, "_scene_error_label"):
                            frame._scene_error_label.config(text=msg)
                    except Exception as e:
                        print(f"Szene {idx} Fehleranzeige fehlgeschlagen:", e)
                else:
                    try:
                        frame = self.scene_tab.scene_tabs[idx]
                        if hasattr(frame, "_scene_error_label"):
                            frame._scene_error_label.config(text="")
                    except:
                        pass

            elif scene.get("type") == "#draw":
                num_points = len(scene.get("drawn_points", []))
                available = config["num_drones"]
                frame = self.scene_tab.scene_tabs[idx]
                # Zu wenige Drohnen (mehr Punkte als Drohnen)
                if num_points > available:
                    has_scene_error = True
                    msg = f"❌ Für die gezeichnete Formation brauchst du {num_points} Drohnen, aber nur {available} verfügbar."
                    scene_errors.append(msg)
                    if hasattr(frame, "_scene_error_label"):
                        frame._scene_error_label.config(text=msg)
                else:
                    if hasattr(frame, "_scene_error_label"):
                        frame._scene_error_label.config(text="")

        # Globale Fehleranzeige
        if has_scene_error:
            self.error_display.show_error("Einige Szenen benötigen mehr Drohnen als verfügbar:")
            for msg in scene_errors:
                self.error_display.show_error(msg)
            return
        run_simulation(config)

    def export_project(self):
        """
        Öffnet einen Speicherdialog und exportiert die aktuelle Projektkonfiguration als JSON-Datei.
        """
        if not self.scene_tab:
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Projektdateien", "*.json")])
        if path:
            config = self.scene_tab.get_full_config()
            project_manager.save_project_json(config, path)
            messagebox.showinfo("Gespeichert", f"Projekt gespeichert:\n{path}")

    def import_project(self):
        """
        Öffnet einen Datei-Auswahldialog, lädt ein Projekt und füllt die GUI entsprechend.
        """
        path = filedialog.askopenfilename(filetypes=[("Projektdateien", "*.json")])
        if path:
            config = project_manager.load_project_json(path)
            self.create_first_scene()
            self.scene_tab.load_from_config(config)
            messagebox.showinfo("Geladen", f"Projekt geladen:\n{path}")
            if "drone-model" in config:
                self.drone_config.set_selected_model(config["drone-model"])
            if "bg-theme" in config:
                self.background_panel.theme_var.set(config["bg-theme"])
            if "num_drones" in config:
                self.drone_config.set_num_drones(config["num_drones"])

    def ask_to_save_before_exit(self):
        """
        Fragt beim Beenden, ob das aktuelle Projekt gespeichert werden soll.
        Reagiert entsprechend auf die Auswahl.
        """
        answer = messagebox.askyesnocancel("Beenden",
                                           "Möchtest du dein Projekt speichern, bevor du das Programm schließt?")
        if answer is True:
            self.export_project()
            self.destroy()
        elif answer is False:
            self.destroy()

    def refresh_project_list(self):
        """
        Listet alle gespeicherten Projekte im Projektverzeichnis im Listbox-Menü auf.
        """
        os.makedirs(PROJECTS_DIR, exist_ok=True)
        self.project_listbox.delete(0, tk.END)
        for filename in os.listdir(PROJECTS_DIR):
            if filename.endswith(".json"):
                self.project_listbox.insert(tk.END, filename)

    def on_project_select(self, event):
        """
        Wird ausgelöst, wenn ein Projekt aus der Sidebar-Liste ausgewählt wird.

        Args:
            event (tk.Event): Das Event-Objekt von Tkinter beim Listbox-Select.
        """
        selection = self.project_listbox.curselection()
        if selection:
            filename = self.project_listbox.get(selection[0])
            path = os.path.join(PROJECTS_DIR, filename)
            config = project_manager.load_project_json(path)
            self.create_first_scene()
            self.scene_tab.load_from_config(config)
            self.current_project_path = path
            self.project_label.config(text=f"Projekt: {os.path.basename(path)}")

    def new_project_dialog(self):
        """
        Öffnet einen Dialog zur Auswahl: neues Projekt erstellen oder ein bestehendes importieren.
        """
        dialog = tk.Toplevel(self)
        dialog.title("Neues Projekt")
        dialog.geometry("300x120")
        dialog.resizable(False, False)

        tk.Label(dialog, text="Was möchtest du tun?", font=("Arial", 11)).pack(pady=10)

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Projekt importieren", width=22,
                  command=lambda: self._import_from_dialog(dialog)).pack(pady=2)
        tk.Button(btn_frame, text="Neues Projekt erstellen", width=22,
                  command=lambda: self._create_new_from_dialog(dialog)).pack(pady=2)

    def _import_from_dialog(self, dialog_window):
        """
        Beendet den Auswahl-Dialog und startet den Importprozess.

        Args:
            dialog_window (tk.Toplevel): Das Fenster, das geschlossen werden soll.
        """
        dialog_window.destroy()
        self.import_project()

    def _create_new_from_dialog(self, dialog_window):
        """
        Erstellt ein neues leeres Projekt und speichert es sofort unter dem angegebenen Namen.

        Args:
            dialog_window (tk.Toplevel): Das Fenster, das geschlossen werden soll.
        """
        dialog_window.destroy()
        name = simpledialog.askstring("Projektname", "Wie soll das neue Projekt heißen?")

        if name:
            config = {
                "num_drones": self.drone_config.get_num_drones(),
                "bg-theme": self.background_panel.theme_var.get(),
                "drone-model": self.drone_config.get_selected_model(),
                "scenes": []
            }
            self.create_first_scene()
            self.scene_tab.load_from_config(config)

            path = os.path.join(PROJECTS_DIR, name + ".json")
            project_manager.save_project_json(config, path)

            self.current_project_path = path
            self.project_label.config(text=f"Projekt: {os.path.basename(path)}")
            self.refresh_project_list()

            messagebox.showinfo("Erstellt", f"Projekt {name} wurde gespeichert.")

    def save_project(self):
        """
        Speichert Projektdaten in eine JSON-Datei.
        """
        if not self.scene_tab or not self.current_project_path:
            messagebox.showerror("Fehler", "Kein aktives Projekt zum Speichern.")
            return

        self.scene_tab.global_config["num_drones"] = self.drone_config.get_num_drones()
        self.scene_tab.global_config["bg-theme"] = self.background_panel.theme_var.get()
        self.scene_tab.global_config["drone-model"] = self.drone_config.get_selected_model()

        config = self.scene_tab.get_full_config()
        project_manager.save_project_json(config, self.current_project_path)

        self.project_label.config(text=f" Projekt: {os.path.basename(self.current_project_path)}")


def get_drones_from_entry(self):
    """
    Liest die Anzahl Drohnen aus einem Entry-Feld.

    Returns:
        int: Eingegebene Drohnenanzahl oder 20 bei ungültiger Eingabe.
    """
    try:
        return int(self.num_drones_entry.get())
    except:
        return 20


def create_gui(on_abort_simulation=None):
    """
    Erzeugt und startet die GUI und gibt bei Erfolg die vollständige Konfiguration zurück.

    Args:
        on_abort_simulation (Optional[Callable]): Optionaler Callback bei Abbruch der Simulation.
        """
    app = GUIController()
    app.run()
    if app.scene_tab:
        return app.scene_tab.get_full_config()
    return None



