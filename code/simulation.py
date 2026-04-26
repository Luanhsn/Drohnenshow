from drone_control import draw_character, change_drone_model, regroup_drones_for_new_text
from theme import changeTheme
from utils import set_camera, select_drawn_points
from formation import Formation
from light import add_light_marker, set_marker_color
import shapes
import movement
import pybullet as p
import pybullet_data
import time
import threading
import numpy as np
import os
import animated_formations

simulation_stop_event = threading.Event()
sim_thread = None

# Liste zum Speichern der Marker-IDs
light_markers = []


def handle_keyboard_input(p, keys, cam_yaw, cam_pitch, cam_distance, cam_target, set_camera):
    cam_changed = False
    if p.B3G_LEFT_ARROW in keys and keys[p.B3G_LEFT_ARROW] & p.KEY_IS_DOWN:
        cam_yaw -= 2
        cam_changed = True
    if p.B3G_RIGHT_ARROW in keys and keys[p.B3G_RIGHT_ARROW] & p.KEY_IS_DOWN:
        cam_yaw += 2
        cam_changed = True
    if p.B3G_UP_ARROW in keys and keys[p.B3G_UP_ARROW] & p.KEY_IS_DOWN:
        cam_pitch = max(cam_pitch - 1, -89)
        cam_changed = True
    if p.B3G_DOWN_ARROW in keys and keys[p.B3G_DOWN_ARROW] & p.KEY_IS_DOWN:
        cam_pitch = min(cam_pitch + 1, -10)
        cam_changed = True
    if ord('1') in keys and keys[ord('1')] & p.KEY_WAS_TRIGGERED:
        cam_distance = max(3, cam_distance - 1)
        cam_changed = True
    if ord('2') in keys and keys[ord('2')] & p.KEY_WAS_TRIGGERED:
        cam_distance = min(50, cam_distance + 1)
        cam_changed = True
    if cam_changed:
        set_camera(cam_yaw, cam_pitch, cam_distance, cam_target)
    return cam_yaw, cam_pitch, cam_distance


def run_simulation(config):
    """
    Startet die Drohnensimulation mit gegebener Konfiguration.
    Stellt durch try...finally sicher, dass die Verbindung immer geschlossen wird.
    """
    global light_markers
    light_markers = []

    p.connect(p.GUI)

    try:
        # Debug-GUI-Elemente für saubere Anzeige entfernen
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.configureDebugVisualizer(p.COV_ENABLE_RGB_BUFFER_PREVIEW, 0)
        p.configureDebugVisualizer(p.COV_ENABLE_DEPTH_BUFFER_PREVIEW, 0)
        p.configureDebugVisualizer(p.COV_ENABLE_SEGMENTATION_MARK_PREVIEW, 0)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        plane_id = p.loadURDF("plane.urdf")

        num_drones = config["num_drones"]
        scenes = config["scenes"]
        changeTheme(config, plane_id)
        drone_path = change_drone_model(config)
        formation = Formation()

        # Startzeiten für jede Szene berechnen
        scene_start_times = []
        time_acc = 0
        for scene in scenes:
            scene_start_times.append(time_acc)
            try:
                duration = float(scene.get("duration", 3.0))
                if duration <= 0: duration = 3.0
            except:
                duration = 3.0
            time_acc += duration

        # Drohnen erzeugen
        all_drones = []
        init_positions = shapes.line_formation(num_drones=num_drones, spacing=1.2, z_height=1.5, y_offset=0.0)
        for pos in init_positions:
            drone_id = p.loadURDF(drone_path, basePosition=pos, useFixedBase=False)
            all_drones.append(drone_id)

        if not scenes:
            print("Keine Szenen definiert. Simulation wird beendet.")
            return

        # Initiales Setup für die erste Szene
        current_scene = scenes[0]
        current_scene_index = 0
        print(f"[0.00s] Aktiviere Szene 1: {current_scene['type']}")


        drone_targets = compute_targets(current_scene, num_drones, formation)
        num_active_drones = len(drone_targets)
        unused_drones = all_drones[num_active_drones:]


        cam_yaw, cam_pitch, cam_distance, cam_target = 45, -30, 18, [0, 0, 2]
        step_counter = 0

        # Licht-Marker erzeugen
        offset = (0, 0, 0.1)
        first_scene_color = scenes[0].get("light", {}).get("color", (1, 1, 0, 1))
        for drone_id in all_drones:
            pos, _ = p.getBasePositionAndOrientation(drone_id)
            marker_pos = tuple(np.array(pos) + np.array(offset))
            marker_id = add_light_marker(marker_pos, color=first_scene_color)
            light_markers.append(marker_id)

        while not simulation_stop_event.is_set():
            keys = p.getKeyboardEvents()
            cam_yaw, cam_pitch, cam_distance = handle_keyboard_input(p, keys, cam_yaw, cam_pitch, cam_distance,
                                                                     cam_target, set_camera)
            p.stepSimulation()
            time.sleep(1.0 / 240.0)
            t = step_counter / 240.0

            if current_scene["type"].startswith("ANIM:"):
                positions = []
                if current_scene["type"] == "ANIM:Wasserfall":
                    positions = animated_formations.waterfall_effect(num_drones, step_counter)
                elif current_scene["type"] == "ANIM:Pulsieren":
                    positions = animated_formations.pulsating_circle(num_drones, step_counter)
                elif current_scene["type"] == "ANIM:Spiral-Helix":
                    positions = animated_formations.spiraling_helix(num_drones, step_counter)

                for i, drone_id in enumerate(all_drones):
                    pos, ori = p.getBasePositionAndOrientation(drone_id)
                    if i < len(positions):
                        target = positions[i]
                        new_pos = movement.interpolate(pos, target, 0.05)
                        p.resetBasePositionAndOrientation(drone_id, new_pos, ori)

            else:
                # Aktive Drohnen zu ihren Zielen bewegen
                for i, drone_id in enumerate(all_drones):
                    if i < len(drone_targets):
                        pos, ori = p.getBasePositionAndOrientation(drone_id)
                        target = drone_targets[i]
                        new_pos = movement.interpolate(pos, target, 0.05)
                        p.resetBasePositionAndOrientation(drone_id, new_pos, ori)

                # Ungenutzte Drohnen sicher parken
                for i, drone_id in enumerate(unused_drones):
                    pos, ori = p.getBasePositionAndOrientation(drone_id)
                    idle_target = [15 + (i % 10) * 1.5, -10 + (i // 10) * 2, 0.5] # Parkposition in einem Raster
                    new_pos = movement.interpolate(pos, idle_target, 0.05)
                    p.resetBasePositionAndOrientation(drone_id, new_pos, ori)

            step_counter += 1

            # Szenenwechsel prüfen
            if current_scene_index + 1 < len(scenes):
                if t >= scene_start_times[current_scene_index + 1]:
                    current_scene_index += 1
                    current_scene = scenes[current_scene_index]
                    print(f"[{t:.2f}s] Aktiviere Szene {current_scene_index + 1}: {current_scene['type']}")

                    color = current_scene.get("light", {}).get("color", (1, 1, 0, 1))
                    for marker_id in light_markers:
                        set_marker_color(marker_id, color)


                    drone_targets = compute_targets(current_scene, num_drones, formation)
                    num_active_drones = len(drone_targets)
                    unused_drones = all_drones[num_active_drones:] # Alle übrigen Drohnen sind ungenutzt


            # Licht-Marker bewegen
            for i, drone_id in enumerate(all_drones):
                pos, _ = p.getBasePositionAndOrientation(drone_id)
                marker_pos = tuple(np.array(pos) + np.array(offset))
                p.resetBasePositionAndOrientation(light_markers[i], marker_pos, [0, 0, 0, 1])

    finally:
        if p.isConnected():
            p.disconnect()
        print("PyBullet-Verbindung wurde sicher getrennt.")


def compute_targets(scene, num_drones, formation):
    """
    Berechnet Zielkoordinaten für Drohnen basierend auf Szene-Typ.
    """
    typ = scene["type"]
    if typ == "#text":
        word = scene.get("text", "")
        if not word: return []
        full_coords = []
        offset = -2.0 * (len(word.replace(' ', '')) / 2.0)
        for char in word:
            if char != " ":
                coords = draw_character(char, z_height=3, y_offset=offset)
                if coords: full_coords.extend(coords)
                offset += 4
        return full_coords

    elif typ == "#image":
        path = scene.get("image_path")
        if path and os.path.exists(path):
            pts, _ = shapes.image_formation(path, target_drones=num_drones)
            return pts
        return []

    elif typ == "#draw":
        pts = scene.get("drawn_points", [])
        if not pts: return []

        def map_point(pt):
            y = (pt[0] / 500) * 10 - 5
            z = 9 - (pt[1] / 500) * 8
            x = 0
            return (x, y, z)

        return [map_point(p) for p in pts]

    elif typ == "#heart":
        return shapes.heart_formation(num_drones, scale_factor=0.15, z_height=3.5)
    elif typ == "#square":
        return shapes.square_formation(num_drones, edge_length=3, center=[1, 2, 1])
    elif typ == "#smile":
        return shapes.smile_face_formation(num_drones, radius=4, z_height=6)
    elif typ == "#circle":
        return shapes.circle_formation(num_drones, radius=4, z_height=4)
    elif typ.startswith("ANIM:"):
        return []

    return [] # Standardmäßig keine Ziele zurückgeben