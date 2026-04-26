import numpy as np


def waterfall_effect(num_drones, step_counter, base_height=2.0):
    """
    Ein Wasserfall-Effekt. Drohnen fallen von oben nach unten und dann wiederholt sich der Zyklus.

    Args:
        num_drones (int): Anzahl der Drohnen.
        step_counter (int): Aktueller Simulationsschritt.
        base_height (float): Die niedrigste Höhe, die die Drohnen erreichen, bevor sie zurückgesetzt werden.
    """
    positions = [] # Drohnenpositionen

    fall_distance = 8.0  # Die gesamte Distanz, die eine Drohne fällt.
    start_height = base_height + fall_distance # Wo sie oben anfangen
    end_height = base_height
    cycle_duration = 400 # Dauer eines kompletten Fallzyklus (in Simulationsschritten)
    horizontal_spread = 8.0 # Maximale Ausbreitung der Drohnen in x-Richtung

    # Erstellt für jede Drohne eine zufällige x,y-Position
    np.random.seed(42) # es kommt immer die gleiche reihenfolge somit ist Simulation reproduzierbar
    drone_xy_positions = [
        (np.random.uniform(-horizontal_spread / 2, horizontal_spread / 2), # gibt eine zufällige Zahl zwischen den beiden Werten zurück
         np.random.uniform(-horizontal_spread / 2, horizontal_spread / 2)) # horizontal_spread / 2 = 4.0, also Zahlen zwischen -4.0 und +4.0
        for i in range(num_drones)
    ]
    np.random.seed() # setzt den Zufallsgenerator zurück auf "wirklich zufällig"

    for i in range(num_drones):
        time_offset = i * (cycle_duration / num_drones) # Jede Drohne startet zu einem anderen Zeitpunkt
        progress = ((step_counter + time_offset) % cycle_duration) / cycle_duration # Wie weit ist die Drohne in ihrem Fall von 0-1?(0 = oben, 1 = unten)
        # Durch % operator: Bei 401 Schritten → springt zurück auf 1, Bei 800 Schritten → springt zurück auf 0, so fallen die Drohnen immer wieder von oben

        # Berechnet die aktuelle Höhe der Drohne
        current_height = start_height - (progress * fall_distance)

        x_pos, y_pos = drone_xy_positions[i]


        # Speichert die komplette 3D-Position (x, y, z)
        positions.append((x_pos, y_pos, current_height))

    return positions


def pulsating_circle(num_drones, step_counter, base_height=5.0):
    """
    Ein Kreis, der seinen Radius ändert.

    Args:
        num_drones (int): Anzahl der Drohnen.
        step_counter (int): Aktueller Simulationsschritt.
        base_height (float): Die konstante Höhe (z-Achse) des Kreismittelpunkts.
    """
    positions = []

    min_radius = 2.0
    max_radius = 7.0
    # Der Kreis wird zwischen 2 und 7 Einheiten groß
    period = 350 # Ein kompletter Puls (groß→klein→groß) dauert 350 Schritte


    phase = (step_counter % period) / period * 2 * np.pi # Das % sorgt wieder dafür, dass es sich wiederholt mit hilfe Sinus Funktion
    # Schritt 0-174: Kreis wird größer sinus steigt von 0 auf 1 und fällt auf 0, Schritt 175-349 Sinus fällt von 0 auf -1 und steigt auf 0: Kreis wird kleiner, 350: Springt zurück auf 0 → Kreis wird wieder größer

    #np.sin() gibt Werte zwischen -1 und +1 zurück, Wir brauchen aber nur positive Werte (0-1) also + 1 * 0.5
    normalized_radius = 0.5 * (1 + np.sin(phase)) #Berechnet wie groß der Kreis gerade ist (zwischen 0 und 1)

    #Wir haben 0-1, brauchen aber 2-7 Meter also Lineare Umrechnung
    current_radius = min_radius + (max_radius - min_radius) * normalized_radius # Wandelt 0-1 um in die Einheiten um (2-7 Meter)

    # Verteile die Drohnen gleichmäßig um den Kreis
    angles = np.linspace(0, 2 * np.pi, num_drones, endpoint=False) # startet bei 0 bis 360° und teilt den Kreis in num_drones teile auf, Das endpoint (360°) nicht mit einbeziehen

    # Koordinaten berechnen:
    for angle in angles: # fur jeden teil des kreises
        # cos() und sin() wandeln Winkel in x,y-Koordinaten um
        x_pos = current_radius * np.cos(angle)
        y_pos = current_radius * np.sin(angle)
        #Je größer der Radius, desto weiter außen die Drohne

        positions.append((x_pos, y_pos, base_height))

    return positions


def spiraling_helix(num_drones, step_counter, base_height=2.0):
    """
    Eine aufsteigende und rotierende Spirale (Helix).

    Args:
        num_drones (int): Anzahl der Drohnen.
        step_counter (int): Aktueller Simulationsschritt.
        base_height (float): Die Starthöhe der Spirale.
    """
    positions = []
    radius = 5.0  # Radius der Spirale
    helix_height = 10.0  # Gesamthöhe der Spirale
    turns = 3  # Anzahl der vollen Umdrehungen
    rotation_speed = 0.005  # Geschwindigkeit, mit der sich die Spirale dreht
    ascent_speed = 0.01  # Geschwindigkeit, mit der die Drohnen aufsteigen

    # Der vertikale Abstand zwischen den Drohnen
    height_step = helix_height / num_drones

    for i in range(num_drones):
        # Startwinkel für jede Drohne, um sie gleichmäßig zu verteilen
        angle_offset = (2 * np.pi * turns / num_drones) * i

        # Aktueller Winkel durch Rotation
        current_angle = step_counter * rotation_speed + angle_offset

        # Aktuelle Höhe der Drohne
        # Die Drohnen steigen auf und werden am oberen Ende wieder nach unten gesetzt
        current_drone_height = base_height + ((i * height_step + step_counter * ascent_speed) % helix_height)

        # Berechne die x- und y-Koordinaten
        x_pos = radius * np.cos(current_angle)
        y_pos = radius * np.sin(current_angle)

        positions.append((x_pos, y_pos, current_drone_height))

    return positions