def draw_character(character, z_height, y_offset):
    """
    Select and call the function that generates drone positions for a given character.

    Args:
        character (str): Character to draw (case-insensitive).
        height (float): Vertical position (height) of the character formation.
        horizontal_offset (float): Horizontal offset (lateral position) of the formation.

    Returns:
        list of tuple: List of 3D position tuples (x, y, z) for the drones forming the character.

    Raises:
        ValueError: If no function is defined for the given character.
    """
    import letters
    char_func = letters.char_to_function.get(character.upper())  # use .upper() for case-insensitivity
    if char_func:
        return char_func(z_height, y_offset)
    else:
        raise ValueError(f"No function defined for character '{character}'")


def change_drone_model(user_input):
    """
    Gets the inputed Drone Model and loads the data Path to the URDF File and returns the excat path to URDF File
    Args:
        user_input: User_input from the Gui
    returns:
        Full Path to the Drone URDF File
    """
    import os
    drone_path = ""
    selected_model = user_input.get("drone-model", "").lower()

    if user_input["drone-model"] == "quadrotor":
        drone_path = os.path.join("models",
                                  "quadrotor.urdf")
    elif user_input["drone-model"] == "mini-drone":
        drone_path = os.path.join("models",
                                  "cf2x.urdf")

    elif user_input["drone-model"] == "white-drone":
        drone_path = os.path.join("models",
                                  "drone.urdf")
    elif user_input["drone-model"] == "simple_drone":
        drone_path = os.path.join("models",
                                  "simple_drone.urdf")
    elif user_input["drone-model"] == "blue-drone":
        drone_path = os.path.join("models", "dragon_ddk_description-master", "dragon_ddk_description-master", "urdf",
                                  "dddk.urdf")
        print("Does the URDF file exist?", os.path.exists(drone_path))
        print("Full path:", os.path.abspath(drone_path))
    elif user_input["drone-model"] == "racer":
        drone_path = os.path.join("models",
                                  "racer.urdf")
    else:
        print(f"Invalid or unhandled Drone Format: '{user_input.get('drone-model')}'")
    return drone_path


def regroup_drones_for_new_text(new_text, existing_drones, formation):
    """
    Reorders a flat list of existing drones into a nested list, according to the number
    of drones needed for each letter in the new text. Extra drones are added as a 'remaining' group.

    Args:
        new_text (str): New text to be formed.
        existing_drones (list): Flat list of drone IDs.
        formation (Formation): Object to get drone counts per letter.

     Returns:
        Tuple: (list of letter-groups, list of unused drones)
    """
    drone_groups = []
    drone_index = 0
    total_available = len(existing_drones)

    for letter in new_text:
        required = formation.get_drone_count(letter)
        group = []

        for _ in range(required):
            if drone_index < total_available:
                group.append(existing_drones[drone_index])
                drone_index += 1
            else:
                print("Nicht genug Drohnen vorhanden.")
                break

        drone_groups.append(group)

    # Remaining drones
    unused_drones = existing_drones[drone_index:] if drone_index < total_available else []

    return drone_groups, unused_drones 