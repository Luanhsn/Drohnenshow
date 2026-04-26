from tkinter import filedialog, messagebox, ttk, Tk
from PIL import Image, ImageTk
import os
import tkinter.colorchooser as colorchooser
from gui.panels.text_formation import TextFormationPanel
from gui.panels.draw_formation_window import DrawFormationWindow


class ImageUploadPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.path = None
        self.preview_label = None


        # Container für den manuellen Upload
        upload_frame = ttk.LabelFrame(self, text="Eigenes Bild hochladen")
        upload_frame.pack(pady=5, padx=5, fill="x")

        self.upload_button = ttk.Button(upload_frame, text="Bild auswählen...", command=self.upload_image)
        self.upload_button.pack(side="left", padx=5, pady=5)

        self.remove_image_button = ttk.Button(upload_frame, text="Bild entfernen", command=self.remove_image)
        self.remove_image_button.pack(side="left", padx=5, pady=5)

        # Container für die vordefinierten Bilder
        predefined_frame = ttk.LabelFrame(self, text="Oder ein vordefiniertes Bild wählen")
        predefined_frame.pack(pady=5, padx=5, fill="x")

        self.predefined_var = tk.StringVar()
        self.predefined_options = ["- Bitte wählen -"]
        self._populate_predefined_images()  # Menü mit Bildnamen füllen

        # Erstellt das Dropdown-Menü
        self.predefined_menu = ttk.OptionMenu(
            predefined_frame,
            self.predefined_var,
            self.predefined_options[0],  # Standardwert
            *self.predefined_options,  # Alle Optionen
            command=self.on_predefined_select
        )
        self.predefined_menu.pack(fill="x", padx=5, pady=5)

        self.status = ttk.Label(self, text="Kein Bild ausgewählt")
        self.status.pack(pady=2)

    def upload_image(self):
        file_types = [('Image Files', '*.png *.jpg *.jpeg *.gif *.bmp *.tiff'), ('All files', '*.*')]
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=file_types)
        if file_path:
            try:
                self.path = file_path
                self.show_preview(file_path)
                self.status.config(text=f"Loaded: {os.path.basename(self.path)}", foreground="green")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {e}")
                self.path = None

    def show_preview(self, file_path):
        if not file_path or not os.path.exists(file_path):
            self.remove_image()
            self.status.config(text="File not found.", foreground="red")
            return
        try:
            img = Image.open(file_path)
            img.thumbnail((200, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            if self.preview_label:
                self.preview_label.destroy()

            self.preview_label = tk.Label(self, image=photo, borderwidth=2, relief="solid")
            self.preview_label.image = photo
            self.preview_label.pack(pady=5)
        except Exception as e:
            if self.preview_label:
                self.preview_label.destroy()
                self.preview_label = None

    def remove_image(self):
        self.path = None
        if self.preview_label:
            self.preview_label.destroy()
            self.preview_label = None
        self.status.config(text="No image selected", foreground="black")

    def get_data(self):
        return {"image_path": self.path}

    def _populate_predefined_images(self):
        """Sucht im Ordner 'predefined_images' nach Bildern und füllt die Optionsliste."""
        image_dir = "predefined_images"
        if os.path.exists(image_dir):
            try:
                # Filtere nach gültigen Bild-Endungen
                valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
                images = [f for f in os.listdir(image_dir) if f.lower().endswith(valid_extensions)]
                if images:
                    self.predefined_options.extend(sorted(images))
            except Exception as e:
                print(f"Fehler beim Lesen des Bilderverzeichnisses: {e}")

    def on_predefined_select(self, selected_image):
        """Wird aufgerufen, wenn ein vordefiniertes Bild aus dem Dropdown gewählt wird."""
        if selected_image == self.predefined_options[0]:  # "- Bitte wählen -"
            return

        try:
            # Konstruiere den Pfad und aktualisiere das Panel
            file_path = os.path.join("predefined_images", selected_image)
            self.path = file_path
            self.show_preview(file_path)
            self.status.config(text=f"Geladen: {os.path.basename(self.path)}", foreground="green")
        except Exception as e:
            messagebox.showerror("Fehler", f"Vordefiniertes Bild konnte nicht geladen werden: {e}")
            self.path = None


from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import tkinter as tk
import tkinter.colorchooser as colorchooser
from tkinter import ttk
from gui.panels.text_formation import TextFormationPanel
from gui.panels.draw_formation_window import DrawFormationWindow


class SceneConfiguratorPanel(ttk.Frame):
    def __init__(self, parent, auto_first_scene=True):
        super().__init__(parent)
        self.scene_tabs = []
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        if auto_first_scene:
            self.add_scene_tab(1)

        self.add_plus_tab()
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.current_scene_index = 0

        # Globale Einstellungen (werden außerhalb von Szenen gesetzt)
        self.global_config = {
            "num_drones": 20,
            "drone-model": "quadrotor",
            "bg-theme": "#standard"
        }

    def add_scene_tab(self, idx):
        """
        Fügt dem Notebook einen neuen Szenen-Tab hinzu.
        Der neue Tab wird immer vor dem "+"-Tab eingefügt.
        """
        frame = ttk.Frame(self.notebook)

        # --- KORREKTUR START ---
        # Die Position ist die des letzten Tabs (des "+"-Tabs)
        # Wenn wir dort einfügen, wird der "+"-Tab nach rechts verschoben.
        # Dies ist robuster, als mit der Länge zu rechnen.
        try:
            insert_pos = len(self.notebook.tabs()) - 1
            self.notebook.insert(insert_pos, frame, text=f"Szene {idx}")
        except tk.TclError:
            # Fängt den Fehler ab, wenn das Notebook leer ist (pos=-1)
            # und fügt den Tab einfach am Ende hinzu.
            self.notebook.add(frame, text=f"Szene {idx}")
        # --- KORREKTUR ENDE ---

        self.scene_tabs.append(frame)

        # Titel
        tk.Label(frame, text=f"Konfiguration für Szene {idx}").pack(pady=10)

        # Szeneninterne Fehleranzeige
        error_label = tk.Label(frame, text="", fg="red", wraplength=450, justify="left")
        error_label.pack()
        frame._scene_error_label = error_label

        # Auswahl Formationstyp
        tk.Label(frame, text="Formationstyp auswählen:").pack()
        type_var = tk.StringVar(value="#text")
        type_options = [
            "#text", "#smile", "#image", "#draw",
            "#heart", "#circle", "#square",
            "ANIM:Wasserfall", "ANIM:Pulsieren", "ANIM:Spiral-Helix"
        ]
        type_menu = tk.OptionMenu(frame, type_var, *type_options,
                                  command=lambda val, f=frame: self.on_type_change(val, f))
        type_menu.pack()

        # Panels
        text_panel = TextFormationPanel(frame)
        image_panel = ImageUploadPanel(frame)

        frame._draw_points = []

        delete_btn = tk.Button(frame, text="🗑️ Szene löschen", fg="red", command=lambda: self.remove_scene_tab(frame))
        delete_btn.pack(anchor="e", pady=5)

        def open_draw_window():
            from tkinter import simpledialog
            from gui.panels.draw_formation_window import DrawFormationWindow
            def on_done(points):
                frame._draw_points = list(points)

            DrawFormationWindow(self, points=frame._draw_points, on_done=on_done)

        draw_btn = tk.Button(frame, text="Formation zeichnen...", command=open_draw_window)
        frame._draw_btn = draw_btn
        frame._draw_points = []

        # Licht farbauswahl
        color_var = tk.StringVar(value="#ffff00")  # Standardfarbe Gelb



        def choose_color():
            color_code = colorchooser.askcolor(title="Lichtfarbe wählen", initialcolor=color_var.get())
            if color_code and color_code[1]:
                color_var.set(color_code[1])
                color_btn.config(bg=color_code[1])

        color_btn = tk.Button(frame, text="Lichtfarbe wählen", bg=color_var.get(), command=choose_color)
        color_btn.pack(pady=5)
        frame._color_var = color_var
        frame._color_btn = color_btn

        # Eingabe für Dauer der Szene
        duration_label = tk.Label(frame, text="Dauer der Szene (in Sekunden):")
        duration_entry = tk.Entry(frame)
        duration_label.pack()
        duration_entry.pack()
        frame._duration_entry = duration_entry

        # Speichern für Zugriff
        frame._type_var = type_var
        frame._text_panel = text_panel
        frame._image_panel = image_panel

        self.on_type_change("#text", frame)

    def on_type_change(self, value, frame):
        """
        Aktualisiert die angezeigten Eingabepanels je nach gewähltem Formationstyp.

        Args:
            value (str): Der gewählte Formationstyp (z. B. "#text", "#image").
            frame (tk.Frame): Das Szenen-Frame, dessen Panels aktualisiert werden.
        """
        frame._text_panel.pack_forget()
        frame._image_panel.pack_forget()
        frame._draw_btn.pack_forget()

        if value == "#text":
            frame._text_panel.pack(pady=5)
        elif value == "#image":
            frame._image_panel.pack(pady=5)
        elif value == "#draw":
            frame._draw_btn.pack(pady=5)
        # Bei #heart, #circle, etc. oder ANIM:... wird kein Panel angezeigt

    def add_plus_tab(self):
        """
        Fügt einen "+"-Tab zum Notebook hinzu, um neue Szenen anzulegen.
        """
        plus_tab = ttk.Frame(self.notebook)
        self.notebook.add(plus_tab, text="+")

    def on_tab_changed(self, event):
        """
        Wird ausgelöst beim Wechsel des Tabs. Fügt bei Klick auf "+"-Tab eine neue Szene hinzu.

        Args:
            event (tk.Event): Das Event-Objekt von Tkinter.
        """
        selected_index = self.notebook.index("current")
        # Check if the last tab (+ tab) is selected
        if selected_index == len(self.notebook.tabs()) - 1:
            new_scene_index = len(self.scene_tabs) + 1
            self.add_scene_tab(new_scene_index)
            # select the newly added tab
            self.notebook.select(len(self.notebook.tabs()) - 2)

    def get_all_scene_data(self):
        """
            Sammelt die Konfigurationsdaten aller Szenen-Tabs.

            Returns:
                list[dict]: Eine Liste von Szenen-Dictionaries mit Typ, Dauer und Inhalt.
            """
        scene_data = []
        for frame in self.scene_tabs:
            typ = frame._type_var.get()
            duration = frame._duration_entry.get()
            try:
                duration_val = float(duration.replace(",", ".").strip())
                if duration_val <= 0:
                    duration_val = 3.0
            except:
                duration_val = 3.0

            data = {"type": typ, "duration": duration_val}

            if typ == "#text":
                data.update(frame._text_panel.get_data())
            elif typ == "#image":
                data.update(frame._image_panel.get_data())
            elif typ == "#draw":
                data["drawn_points"] = getattr(frame, "_draw_points", [])
            elif typ in ("#heart", "#circle", "#square", "ANIM:Wasserfall", "ANIM:Pulsieren"):
                data["content"] = typ  # Speichere Formation oder Animation direkt als content
            else:
                data["content"] = "undefined"

            # Farbe als RGBA speichern (Hex nach RGBA umwandeln)
            hex_color = frame._color_var.get()
            rgb = self.hex_to_rgba(hex_color)
            data["light"] = {"color": rgb}

            scene_data.append(data)
        return scene_data

    def hex_to_rgba(self, hex_color):
        hex_color = hex_color.lstrip("#")
        lv = len(hex_color)
        rgb = tuple(int(hex_color[i:i + lv // 3], 16) / 255.0 for i in range(0, lv, lv // 3))
        return tuple(list(rgb) + [1.0])  # Alpha immer 1.0

    def get_full_config(self):
        """
        Erzeugt die vollständige Konfiguration für die Simulation.

        Returns:
            dict: Globale Konfiguration kombiniert mit allen Szenendaten.
        """
        return {
            **self.global_config,
            "scenes": self.get_all_scene_data()
        }

    def get_current_scene(self):
        """
        Gibt das aktuell ausgewählte Szenen-Frame zurück, falls vorhanden.
        """
        if 0 <= self.current_scene_index < len(self.scene_tabs):
            return self.scene_tabs[self.current_scene_index]
        return None

    def load_from_config(self, config):
        """
        Lädt eine bestehende Konfiguration in das Panel.

        Args:
            config (dict): Die Projektkonfiguration mit globalen Werten und Szenenliste.
        """
        self.clear_all_scenes()

        # Temporär deaktivieren Tab-Changed-Verhalten
        self.loading = True

        for scene in config.get("scenes", []):
            self.add_scene_from_data(scene)

        self.loading = False  # wieder aktivieren

        # Stellt sicher, dass ein echter Szenen-Tab ausgewählt ist
        if self.scene_tabs:
            self.notebook.select(self.scene_tabs[0])
            self.current_scene_index = 0

        # globale Config updaten – falls nötig
        self.global_config["num_drones"] = config.get("num_drones", 30)
        self.global_config["bg-theme"] = config.get("bg-theme", "#standard")
        self.global_config["drone-model"] = config.get("drone-model", "quadrotor")

    def add_scene_from_data(self, scene):
        """
        Fügt eine Szene aus einem gegebenen Dictionary als neuen Tab hinzu.

        Args:
            scene (dict): Ein Dictionary mit z. B. "type", "duration", "text" oder "image_path".
        """
        idx = len(self.scene_tabs) + 1
        self.add_scene_tab(idx)
        frame = self.scene_tabs[-1]

        typ = scene.get("type", "#text")
        frame._type_var.set(typ)
        self.on_type_change(typ, frame)

        frame._duration_entry.delete(0, "end")
        frame._duration_entry.insert(0, str(scene.get("duration", 3.0)))
        frame._light_data = scene.get("light", None)

        if typ == "#text":
            frame._text_panel.input_var.set(scene.get("text", ""))
        elif typ == "#image":
            path = scene.get("image_path", None)
            if path:
                # Directly update the panel's state
                frame._image_panel.path = path
                frame._image_panel.status.config(text=f"Loaded: {os.path.basename(path)}", foreground="green")
                frame._image_panel.show_preview(path)
            else:
                # Ensure the panel is cleared if no path
                frame._image_panel.remove_image()
        elif typ == "#draw" and "drawn_points" in scene:
            frame._draw_points = scene["drawn_points"]
        else:
            pass  # für #heart, #circle etc. kein Panel

        if "light" in scene and "color" in scene["light"]:
            rgba = scene["light"]["color"]
            hex_color = '#%02x%02x%02x' % tuple(int(c * 255) for c in rgba[:3])
            frame._color_var.set(hex_color)
            frame._color_btn.config(bg=hex_color)


    def remove_scene_tab(self, frame):
        """
        Entfernt einen bestimmten Szenen-Tab und aktualisiert die Tab-Beschriftungen.

        Args:
            frame (tk.Frame): Das zu entfernende Szenen-Frame.
        """
        if frame in self.scene_tabs:
            idx = self.scene_tabs.index(frame)
            self.scene_tabs.remove(frame)
            try:
                index = self.notebook.index(frame)  # ✅ korrektes Objekt
                self.notebook.forget(index)
            except Exception as e:
                print(f"Fehler beim Entfernen des Tabs: {e}")
            frame.destroy()

            # Neuer aktueller Tab setzen
            if self.scene_tabs:
                self.notebook.select(self.scene_tabs[-1])  # letzte Szene auswählen
                self.current_scene_index = len(self.scene_tabs) - 1
            else:
                self.current_scene_index = -1

    def clear_all_scenes(self):
        """
        Entfernt alle Szenen-Tabs aus dem Notebook, bis auf den "+" Tab.
        """
        for tab_id in self.notebook.tabs():
            self.notebook.forget(tab_id)
        self.scene_tabs.clear()
        self.add_plus_tab()
        self.current_scene_index = 0

    def set_num_drones(self, value):
        """
        Setzt die Drohnenanzahl in der globalen Konfiguration.

        Args:
            value (int): Neue Anzahl der Drohnen.
        """
        self.num_var.set(str(value))

    def update_current_scene_data(self):
        """Überträgt GUI-Eingaben der aktuellen Szene in die Szene-Tab-Struktur."""
        frame = self.get_current_scene()
        if not frame:
            return

        typ = frame._type_var.get()
        frame._scene_data = {
            "type": typ,
            "duration": self._safe_float(frame._duration_entry.get(), default=3.0)
        }

        if typ == "#text":
            frame._scene_data.update(frame._text_panel.get_data())
        elif typ == "#image":
            frame._scene_data.update(frame._image_panel.get_data())
        elif typ == "#draw":
            frame._scene_data.update(frame._draw_panel.get_data())
        elif typ in ("#heart", "#circle", "#square", "ANIM:Wasserfall", "ANIM:Pulsieren"):
            frame._scene_data["content"] = typ
        else:
            frame._scene_data["content"] = "undefined"

    def _safe_float(self, val, default=3.0):
        """
        Konvertiert einen Eingabewert sicher in einen Float.

        Args:
            val (str): Der zu konvertierende Stringwert.
            default (float): Fallback-Wert bei Fehler.

        Returns:
            float: Der konvertierte Wert oder der Fallback.
        """
        try:
            return float(str(val).replace(",", ".").strip())
        except:
            return default


