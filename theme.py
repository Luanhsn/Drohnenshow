import random
import math
import pybullet as p
def create_starry_sky(num_stars=300, sky_radius_min=40, sky_radius_max=60, star_size_min=0.03, star_size_max=0.08):
    """
       Creates a realistic starry sky background in the simulation environment.

       Args:
           num_stars (int): Number of stars to generate
           sky_radius_min (float): Minimum distance from origin for stars
           sky_radius_max (float): Maximum distance from origin for stars
           star_size_min (float): Minimum star size (radius)
           star_size_max (float): Maximum star size (radius)


       Effects:
           - Creates visual sphere objects distributed in a hemisphere
           - Uses size and color variations for realism
           - Optimizes by reusing visual shapes for same-sized stars
       """

    star_color_base = [0.95, 0.95, 0.85, 1.0] # Farbe der sterne

    print(f"Erstelle {num_stars} Sterne...")
    star_visual_shape_ids = {} # Dictionary, um visuelle Formen für verschiedene Größen zu speichern und wiederzuverwenden

    for i in range(num_stars):

        # Zufällige Größe für den Stern mit random modul
        current_star_size = random.uniform(star_size_min, star_size_max)

        # Visuelle Form erstellen oder wiederverwenden

        rounded_size_key = round(current_star_size, 3) #  Größe der Form
        if rounded_size_key not in star_visual_shape_ids:
            #  Variation in der Sternfarbe
            color_variation = random.uniform(-0.05, 0.05)
            r = max(0, min(1, star_color_base[0] + color_variation))
            g = max(0, min(1, star_color_base[1] + color_variation))
            b = max(0, min(1, star_color_base[2] + color_variation - random.uniform(0,0.1))) # Manche etwas bläulicher

            # stern objekte erstellen
            star_visual_shape_ids[rounded_size_key] = p.createVisualShape(
                shapeType=p.GEOM_SPHERE, # rundes objekt
                radius=current_star_size,
                rgbaColor=[r,g,b, star_color_base[3]],
                specularColor=[0,0,0] # Sterne sollten nicht glänzen
            )
        visual_shape_id = star_visual_shape_ids[rounded_size_key]

        # Zufällige Position auf einer Halbkugel
        sky_radius = random.uniform(sky_radius_min, sky_radius_max) # einige Sterne erscheinen näher einige weiter weg jeder Stern hat unterschiedlichen Radius
        phi = random.uniform(0, 2 * math.pi) # Winkel (0 bis 360 Grad)

        # Theta für Halbkugel (0 bis 90 Grad)
        # cos_theta = random.uniform(0, 1) # Nur obere Halbkugel
        # Theta für fast ganze Kugel, aber leicht über dem Horizont
        cos_theta = random.uniform(-0.1, 1) # Von knapp unter Horizont
        theta = math.acos(cos_theta) # Polarwinkel

        # Konvertiere in kartesische Koordinaten
        x = sky_radius * math.sin(theta) * math.cos(phi)
        y = sky_radius * math.sin(theta) * math.sin(phi)
        z = sky_radius * math.cos(theta)
        p.createMultiBody(
            baseMass=0, # Keine Masse, rein visuell
            baseCollisionShapeIndex=-1, # Keine Kollision
            baseVisualShapeIndex=visual_shape_id,
            basePosition=[x, y, z]
        )
    print("Sternenhimmel erstellt.")

def changeTheme(user_input_string, planeId):
    """
       Applies visual theme changes based on user selection.

       Args:
           user_input_string (dict): GUI parameters including "bg-theme"
           planeId (int): PyBullet ID of the ground plane

       Effects:
           - For "#dark": Darkens ground and sets black background
           - For "#stars": Creates starry sky and dark ground
           - Disables GUI controls and enables shadows for both themes

       Note:
           Removes default plane for "#stars" theme and creates custom dark ground
       """
    import pybullet as p
    if user_input_string["bg-theme"] != "#standard":

        if user_input_string["bg-theme"] == "#dark":

            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)  # pybullet steuerelemente ausblenden

            p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)  # schatten aktivieren

            p.changeVisualShape(planeId, -1, rgbaColor=[0.15, 0.15, 0.18, 1])  # Boden dunkler machen

            p.changeVisualShape(planeId, -1, specularColor=[0.1, 0.1, 0.1])

            tiefschwarz_himmel = [0.0, 0.0, 0.0]
            p.configureDebugVisualizer(rgbBackground=tiefschwarz_himmel)
        elif user_input_string["bg-theme"] == "#stars":

            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)  # pybullet steuerelemente ausblenden

            p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)  # schatten aktivieren
            tiefschwarz_himmel = [0.0, 0.0, 0.0]
            p.configureDebugVisualizer(rgbBackground=tiefschwarz_himmel)
            try:
                p.removeBody(planeId)
                print(f"Standardebene (plane.urdf mit ID {planeId}) wurde für das '#stars'-Theme entfernt.")
            except p.error as e:
                print(f"Fehler beim Entfernen der Standardebene (ID: {planeId}) für '#stars'-Theme: {e}")

            # Einen dunklen Boden erstellen damit die Szene insgesamt dunkel wirkt.
            ground_half_extents = [30, 30, 0.05]
            dark_ground_color_rgba = [0.02, 0.02, 0.03, 1.0]  # Sehr dunkler Boden
            dark_ground_specular_color = [0.01, 0.01, 0.01]  # Fast kein Glanz

            ground_collision_shape_id = p.createCollisionShape(shapeType=p.GEOM_BOX, halfExtents=ground_half_extents)
            ground_visual_shape_id = p.createVisualShape(shapeType=p.GEOM_BOX, halfExtents=ground_half_extents,
                                                         rgbaColor=dark_ground_color_rgba)
            ground_body_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=ground_collision_shape_id,
                                               baseVisualShapeIndex=ground_visual_shape_id,
                                               basePosition=[0, 0, -ground_half_extents[2]])
            p.changeVisualShape(ground_body_id, -1, specularColor=dark_ground_specular_color)
            create_starry_sky() 