import tkinter as tk
import math

class DrawFormationWindow(tk.Toplevel):
    def __init__(self, master, points=None, on_done=None):
        super().__init__(master)
        self.title("2D-Formation zeichnen")
        self.canvas_size = 500
        self.canvas = tk.Canvas(self, bg="white", width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack(fill="both", expand=True)
        self.points = list(points) if points else []
        self.on_done = on_done

        self.drone_radius_y = 0.32  # Meter
        self.drone_radius_z = 0.15  # Meter
        self.px_per_meter_y = self.canvas_size / 10
        self.px_per_meter_z = self.canvas_size / 10
        self.drone_radius_y_px = self.drone_radius_y * self.px_per_meter_y
        self.drone_radius_z_px = self.drone_radius_z * self.px_per_meter_z
        self.min_distance_y = 2 * self.drone_radius_y_px
        self.min_distance_z = 2 * self.drone_radius_z_px
        self.grid_spacing = 25

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.add_point)

        btn_frame = tk.Frame(self)
        btn_frame.pack()
        tk.Button(btn_frame, text="Fertig", command=self.finish).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Alle Punkte löschen", command=self.clear_points).pack(side="left", padx=4)

        self.redraw_all()

    def draw_grid(self):
        for x in range(0, self.canvas_size, self.grid_spacing):
            self.canvas.create_line(x, 0, x, self.canvas_size, fill="#e0e0e0")
        for y in range(0, self.canvas_size, self.grid_spacing):
            self.canvas.create_line(0, y, self.canvas_size, y, fill="#e0e0e0")

    def redraw_all(self):
        self.canvas.delete("zone")
        for (x, y) in self.points:
            self.canvas.create_oval(
                x - self.drone_radius_y_px, y - self.drone_radius_z_px,
                x + self.drone_radius_y_px, y + self.drone_radius_z_px,
                outline="blue", width=2, tags="zone"
            )
            self.canvas.create_oval(
                x - self.min_distance_y, y - self.min_distance_z,
                x + self.min_distance_y, y + self.min_distance_z,
                outline="gray", dash=(4, 2), width=2, tags="zone"
            )
            r = 3
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="red", tags="zone")

    def add_point(self, event):
        x, y = event.x, event.y
        for px, py in self.points:
            dx = (x - px) / self.min_distance_y
            dy = (y - py) / self.min_distance_z
            if math.hypot(dx, dy) < 1.0:
                self.bell()
                return
        self.points.append((x, y))
        self.redraw_all()

    def clear_points(self):
        self.points = []
        self.redraw_all()

    def finish(self):
        if self.on_done:
            self.on_done(self.points)
        self.destroy()
