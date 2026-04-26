import numpy as np
from PIL import Image
def line_formation(num_drones, spacing, z_height ,y_offset):
    """
    Generate positions for drones arranged in a horizontal line formation.

    The drones are spaced evenly along the x-axis, centered around zero,
    with a fixed height on the z-axis and an optional lateral offset on the y-axis.

    Parameters:
        num_drones (int): Number of drones in the formation.
        spacing (float): Distance between adjacent drones along the x-axis.
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions.
    """
    positions = []
    start_x = - (num_drones - 1) / 2 * spacing
    for i in range(num_drones):
        x = start_x + i * spacing
        y = 0
        z = z_height
        positions.append((x , y+y_offset  , z))
    return positions


def heart_formation(num_drones, scale_factor, z_height):
    """
    Generate 3D coordinates for drones arranged in a heart-shaped formation.

    The heart shape is created using parametric equations, scaled by
    `scale_factor` and positioned at a fixed height `z_height`.

    Parameters:
        num_drones (int): Number of drones in the formation.
        scale_factor (float): Scaling factor to adjust the size of the heart shape.
        z_height (float): Height (z-coordinate) at which the drones are positioned.

    Returns:
        list: List of [x, y, z] coordinates for each drone position.
    """
    positions = []
    # Teile das Herz in gleiche Stücke auf
    # Generate evenly spaced parameter values from 0 to 2π (excluding endpoint to avoid duplication)
    t_values = np.linspace(0, 2 * np.pi, num_drones, endpoint=False)

    # Herzform erstellen
    for t in t_values:
        # x = 16*sin³(t)
        # z = 13*cos(t) - 5*cos(2t) - 2*cos(3t) - cos(4t) [positive for upright heart]
        #Formeln zeichnen automatisch ein Herz
        x = 16 * (np.sin(t) ** 3) # Breite des Herzens
        z_offset = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t) # Herzform

        # Mache das Herz größer oder kleiner
        x *= scale_factor
        z_offset *= scale_factor

        # Das Herz steht vertikal (x = horizontal, z = vertikal)
        z_pos = z_height + z_offset

        # Speichere die 3D-Position
        positions.append([x, z_height, z_pos])

    # Abstand zwischen Drohnen korrigieren
    min_distance = 1.0 * scale_factor
    offset_step = 0.2 * scale_factor

    # Wiederhole 10 mal, um alle Drohnen richtig zu verteilen
    for iteration in range(10):
        adjustments_made = False

        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                # Vergleiche jede Drohne mit jeder anderen
                dx = positions[i][0] - positions[j][0]
                dz = positions[i][2] - positions[j][2]
                distance = np.sqrt(dx ** 2 + dz ** 2) # Berechne den Abstand zwischen zwei Drohnen, Pythagoras: √(dx² + dz²)

                if distance < min_distance:
                    adjustments_made = True

                    # Calculate how much to separate them
                    needed_separation = min_distance - distance

                    if distance > 0:
                        # Normalizieren des Vektors
                        direction_x = dx / distance
                    else:
                        # If positions are identical, move them in opposite directions
                        direction_x = 1.0  # Move in x direction


                    # Schiebe die Drohnen auseinander mit der hälfte der benötigten Seperation
                    move_distance = (needed_separation / 2) + offset_step
                    # Eine geht nach links, eine nach rechts
                    positions[i][0] += (direction_x * move_distance + 0.2)
                    positions[j][0] -= (direction_x * move_distance + 0.2)

        if not adjustments_made:
            break

    return positions


def square_formation(num_drones, edge_length, center):
    """
    Generate 3D coordinates for drones arranged evenly along the perimeter of a square.

    For up to four drones, positions are placed at the square's corners.
    For more drones, positions are distributed evenly along the square's edges,
    starting from the bottom edge and proceeding clockwise.

    Parameters:
        num_drones (int): Number of drones in the formation.
        edge_length (float): Length of each side of the square.
        center (tuple of float): (x, y, z) coordinates of the square's center.

    Returns:
        list of list: List of [x, y, z] coordinates representing drone positions.
    """
    positions = []
    half = edge_length / 2

    if num_drones <= 4:
        # Für wenige Drohnen, in den Ecken platzieren
        corners = [
            [center[0] - half, center[2], center[1] - half],
            [center[0] + half, center[2], center[1] - half],
            [center[0] + half, center[2], center[1] + half],
            [center[0] - half, center[2], center[1] + half]
        ]
        return corners[:num_drones]

    perimeter = 4 * edge_length  # Umfang des Quadrats
    step = perimeter / num_drones  # Abstand zwischen den Drohnen

    for i in range(num_drones):
        distance = i * step  # Distanz entlang des Umfangs

        if distance <= edge_length:  # Unterkante
            x = center[0] - half + distance
            y = center[1] - half
        elif distance <= 2 * edge_length:  # Rechte Kante
            x = center[0] + half
            y = center[1] - half + (distance - edge_length)
        elif distance <= 3 * edge_length:  # Oberkante
            x = center[0] + half - (distance - 2 * edge_length)
            y = center[1] + half
        else:  # Linke Kante
            x = center[0] - half
            y = center[1] + half - (distance - 3 * edge_length)

        positions.append([x, center[2], y])

    return positions


def circle_formation(num_dornes, radius, z_height, center=(0, 0)):
    """
    Generate 3D coordinates for drones arranged in a circular formation.

    The drones are evenly spaced along the circumference of a circle defined by
    the given radius and centered at the specified (x, y) position. All drones
    are positioned at the same height on the z-axis.

    Parameters:
        num_drones (int): Number of drones in the formation.
        radius (float): Radius of the circle.
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        center (tuple of float, optional): (x, y) coordinates of the circle's center. Default is (0, 0).

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions.

    """
    positions = []
    angles = np.linspace(0, 2 * np.pi, num_dornes, endpoint=False)
    for angle in angles:
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        z = z_height
        positions.append((x, z, y+4.3))
    return positions


def image_formation(image_path, target_drones=500, brightness_threshold=128, scale_factor=0.05, z_height=3.0,
                    y_offset=0.0):
    # ist eher für Bilder von Texten oder einfachen Zeichungen aus Linien mit hohem Kontrast
    """
    Konvertiert ein Bild in 3D-Koordinaten für eine Drohnenformation.

    Args:
        image_path (str): Der Pfad zur Bilddatei.
        target_drones (int): Die maximale Anzahl der zu verwendenden Drohnen.
        brightness_threshold (int): Ein Schwellenwert (0-255). Pixel, die dunkler sind, werden verwendet.
        scale_factor (float): Faktor zur Skalierung der Bildgröße auf die Simulationswelt.
        z_height (float): Die Höhe der Formation in der Simulation.
        y_offset (float): Der seitliche Versatz der Formation.

    Returns:
        tuple: Ein Tupel aus (numpy.ndarray mit den 3D-Koordinaten, Anzahl der Drohnen).
    """
    base_height = 3.0
    #Die Funktion nimmt das Bild, findet alle dunklen Pixel und wandelt deren Positionen in 3D-Koordinaten für die Drohnen um
    try:
        #Bild laden und in Graustufen konvertieren
        img = Image.open(image_path).convert("L")  # "L" = 8-bit Graustufen
        arr = np.array(img)
    except Exception as e:
        print(f"Fehler beim Laden des Bildes: {e}")
        return np.array([]), 0

    # Koordinaten der dunklen Pixel finden die unter dem treshold sind
    # yv und xv sind die Pixel-Indizes
    yv, xv = np.where(arr < brightness_threshold)

    if xv.size == 0:
        print("Warnung: Keine passenden Pixel unter dem Helligkeits-Schwellenwert gefunden.")
        return np.array([]), 0

    #  packt die beiden Listen mit den X- und Y-Positionen zu Liste von Koordinatenpaaren zusammen
    coords = np.column_stack((xv, yv))

    # Anzahl der Drohnen auf target_drones begrenzen
    num_available_pixels = len(coords)

    if num_available_pixels > target_drones:
        step = max(1, num_available_pixels // target_drones)  # step wird berechnet, z.B man hat 5000 Pixel, will aber nur 500 Drohnen, dann wäre der step = 10
        coords = coords[::step] #coords[::step] nimmt dann nur jeden step (z.B 10) Punkt aus der Liste so wird die Form des Bildes in etwa beibehalten, aber mit  weniger Punkten.


    actual_drones = len(coords)
    if actual_drones == 0:
        print("Warnung: Nach der Verarbeitung sind keine Drohnenpositionen übrig geblieben.")
        return np.array([]), 0


    # Koordinaten zentrieren und skalieren
    center = coords.mean(axis=0) #  berechnet den geometrischen Mittelpunkt aller Punkte
    centered_coords = coords - center #ieht diesen Mittelpunkt von jeder einzelnen Koordinate ab, Die ganze Punktwolke ist  um den Nullpunkt (0,0) zentriert


    final_coords_list = []

    # rechnet aus, wo die tiefste Drohne der Formation fliegen würde.
    max_y_coord = centered_coords.max()
    lowest_z = base_height - (max_y_coord * scale_factor) # max wegen der inventierung

    # wenn zu tief wird die gesamte Formation so weit nach oben verschoben, dass die unterste Drohne auf einer Höhe von 0,5 Metern fliegt
    if lowest_z < 0.5:
        height_adjustment = 0.5 - lowest_z
        base_height = base_height + height_adjustment


    # die 2D-Pixelkoordinaten werden in 3D-Weltkoordinaten umgewandelt:
    # x-axis ist die zentrierte X-Koordinate des Pixels, multipliziert mit dem scale_factor
  # z wird aus der Y-Koordinate des Pixels berechnet
    for i in range(actual_drones):
        x = centered_coords[i, 0] * scale_factor  # horizontal in image
        y = y_offset  # constant depth
        z = base_height - (centered_coords[i, 1] * scale_factor)  # base_height - ... sorgt dafür, dass das Bild richtig herum angezeigt wird weil invertiert
        final_coords_list.append([x, y, z])

    final_coords = np.array(final_coords_list)
    return final_coords, actual_drones

def smile_face_formation(num_drones, radius=4.0, z_height=5.5):
    """
    Erzeugt ein Smile-Face mit:
    - Kopfkreis (X-Z-Ebene)
    - Zwei runden Augen
    - Smile-Mund (nach oben gebogen) mit horizontal stehenden Drohnen (X-Achse)
    Alle Drohnen fliegen auf gleicher Tiefe (Y = 0)
    """
    positions = []

    # Aufteilung der Drohnen
    num_circle = int(num_drones * 0.5)  # 50% für den Kopf
    num_eyes = int(num_drones * 0.1)    # 10% für jedes Auge (2 Augen)
    num_mouth = num_drones - num_circle - 2 * num_eyes  # Rest für den Mund

    # --- 1. Kopf-Kreis ---
    angles = np.linspace(0, 2 * np.pi, num_circle, endpoint=False)
    for angle in angles:
        x = radius * np.cos(angle)
        z = z_height + radius * np.sin(angle)
        positions.append([x, 0, z])  # Y = 0

    # --- 2. Augen ---
    eye_radius = 0.3
    eye_offset_x = radius * 0.5
    eye_offset_z = z_height + radius * 0.5
    eye_angles = np.linspace(0, 2 * np.pi, num_eyes, endpoint=False)

    for angle in eye_angles:
        # Linkes Auge
        x1 = -eye_offset_x + eye_radius * np.cos(angle)
        z1 = eye_offset_z + eye_radius * np.sin(angle)
        positions.append([x1, 0, z1])
        # Rechtes Auge
        x2 = eye_offset_x + eye_radius * np.cos(angle)
        z2 = eye_offset_z + eye_radius * np.sin(angle)
        positions.append([x2, 0, z2])

    # --- 3. Mund (Smile in X-Z-Ebene) ---
    mouth_radius = radius * 0.8
    mouth_width = mouth_radius * 2
    start_x = -mouth_width / 2
    step_x = mouth_width / (num_mouth - 1) if num_mouth > 1 else 0

    for i in range(num_mouth):
        x = start_x + i * step_x
        progress = i / (num_mouth - 1) if num_mouth > 1 else 0
        # Smile: Umgekehrte Sinus-Kurve (-sin) für lächelnden Mund
        # Wir verwenden -np.sin, um die Kurve nach oben zu wölben
        smile_height = 0.6 * -np.sin(progress * np.pi)  # Minuszeichen für Lächeln
        z = z_height - 0.8 + smile_height  # Basisposition etwas tiefer
        positions.append([x, 0, z])

    return positions



def smile_face_formation(num_drones, radius=4.0, z_height=5.5):
    """
    Erzeugt ein Smile-Face mit:
    - Kopfkreis (X-Z-Ebene)
    - Zwei runden Augen
    - Smile-Mund (nach oben gebogen) mit horizontal stehenden Drohnen (X-Achse)
    Alle Drohnen fliegen auf gleicher Tiefe (Y = 0)
    """
    positions = []

    # Aufteilung der Drohnen
    num_circle = int(num_drones * 0.5)  # 50% für den Kopf
    num_eyes = int(num_drones * 0.1)    # 10% für jedes Auge (2 Augen)
    num_mouth = num_drones - num_circle - 2 * num_eyes  # Rest für den Mund

    # --- 1. Kopf-Kreis ---
    angles = np.linspace(0, 2 * np.pi, num_circle, endpoint=False)
    for angle in angles:
        x = radius * np.cos(angle)
        z = z_height + radius * np.sin(angle)
        positions.append([x, 0, z])  # Y = 0

    # --- 2. Augen ---
    eye_radius = 0.3
    eye_offset_x = radius * 0.5
    eye_offset_z = z_height + radius * 0.5
    eye_angles = np.linspace(0, 2 * np.pi, num_eyes, endpoint=False)

    for angle in eye_angles:
        # Linkes Auge
        x1 = -eye_offset_x + eye_radius * np.cos(angle)
        z1 = eye_offset_z + eye_radius * np.sin(angle)
        positions.append([x1, 0, z1])
        # Rechtes Auge
        x2 = eye_offset_x + eye_radius * np.cos(angle)
        z2 = eye_offset_z + eye_radius * np.sin(angle)
        positions.append([x2, 0, z2])

    # --- 3. Mund (Smile in X-Z-Ebene) ---
    mouth_radius = radius * 0.8
    mouth_width = mouth_radius * 2
    start_x = -mouth_width / 2
    step_x = mouth_width / (num_mouth - 1) if num_mouth > 1 else 0

    for i in range(num_mouth):
        x = start_x + i * step_x
        progress = i / (num_mouth - 1) if num_mouth > 1 else 0
        # Smile: Umgekehrte Sinus-Kurve (-sin) für lächelnden Mund
        # Wir verwenden -np.sin, um die Kurve nach oben zu wölben
        smile_height = 0.6 * -np.sin(progress * np.pi)  # Minuszeichen für Lächeln
        z = z_height - 0.8 + smile_height  # Basisposition etwas tiefer
        positions.append([x, 0, z])

    return positions