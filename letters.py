import numpy as np

def _sample_points(vertices, n, closed=False):
    """
    Uniformly sample n points along the polyline defined by vertices.
    Ensures minimum distance between drones to prevent collision.
    """
    seg_lengths = []
    min_distance=0.2
    pts = vertices.copy()
    if closed:
        pts = vertices + [vertices[0]]

    for i in range(len(pts) - 1):
        a, b = np.array(pts[i]), np.array(pts[i + 1])
        seg_lengths.append(np.linalg.norm(b - a))
    total_len = sum(seg_lengths)

    # Compute number of drones based on total length and min_distance
    max_drones = int(total_len / min_distance)
    n = min(n, max_drones)

    distances = np.linspace(0, total_len, n, endpoint=False)
    positions = []
    seg_cum = np.cumsum([0] + seg_lengths)

    for d in distances:
        idx = np.searchsorted(seg_cum, d, side='right') - 1
        t = (d - seg_cum[idx]) / seg_lengths[idx]
        p0, p1 = np.array(pts[idx]), np.array(pts[idx + 1])
        pos = p0 + (p1 - p0) * t
        positions.append(tuple(pos))

    return positions

def _sample_points2(vertices, n, closed=False):
    """
    Uniformly sample n points along the polyline defined by vertices.
    If closed=True, treats the shape as closed (connects last->first).
    """
    # Compute segment lengths
    seg_lengths = []
    pts = vertices.copy()
    if closed:
        pts = vertices + [vertices[0]]
    for i in range(len(pts) - 1):
        a, b = np.array(pts[i]), np.array(pts[i+1])
        seg_lengths.append(np.linalg.norm(b - a))
    total_len = sum(seg_lengths)
    # sample distances
    distances = np.linspace(0, total_len, n, endpoint=False)
    positions = []
    seg_cum = np.cumsum([0] + seg_lengths)
    for d in distances:
        # find segment index
        idx = np.searchsorted(seg_cum, d, side='right') - 1
        t = (d - seg_cum[idx]) / seg_lengths[idx]
        p0, p1 = np.array(pts[idx]), np.array(pts[idx+1])
        pos = p0 + (p1 - p0) * t
        positions.append(tuple(pos))
    return positions
###########################################


def rotate_to_vertical(positions):
    return [(x, z, y) for (x, y, z) in positions]


def A_formation_vertical(z_height, y_offset):
    """
    Generates a proportional vertical 'A' formation using 11 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'A' formation.
    """
    positions = []

    # crossbar postion
    positions.append((0,y_offset,z_height+1))

    # left leg
    for i in range(5):
        x_coordinate = 0
        y_coordinate = y_offset - 1/3 - i/6
        z_coordinate = z_height + 2 - i/4 * 2
        positions.append((x_coordinate, y_coordinate, z_coordinate))
    # right leg
    for i in range(5):
        x_coordinate = 0
        y_coordinate = y_offset + 1/3 + i/6
        z_coordinate = z_height + 2 - i/4 * 2
        positions.append((x_coordinate,y_coordinate,z_coordinate))

    return positions


def B_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'B' formation using 14 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'B' formation.
    """

    positions = []

    # vertical spine
    for i in range(5):
        x_coordinate = 0
        y_coordinate = y_offset - 0.775
        z_coordinate = z_height + 2 - i/2
        positions.append((x_coordinate,y_coordinate,z_coordinate))

    # top curve
    top_angles = np.linspace(np.pi * 17/36, -np.pi * 17/36, 5)

    for angle in top_angles:
        x_coordinate = 0
        y_coordinate = y_offset - 0.225 + 1 * np.cos(angle)
        z_coordinate = z_height + 1.5 + 0.5 * np.sin(angle)
        positions.append((x_coordinate,y_coordinate,z_coordinate))

    # bottom curve
    bottom_angles = np.linspace(np.pi * 17/72, -np.pi * 17/36, 4)

    for angle in bottom_angles:
        x_coordinate = 0
        y_coordinate = y_offset - 0.225 + 1 * np.cos(angle)
        z_coordinate = z_height + 0.5 + 0.5 * np.sin(angle)
        positions.append((x_coordinate,y_coordinate,z_coordinate))

    return positions


def C_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'C' formation using 9 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'C' formation.
    """
    radius = 1.1  # incresed from standard 1 for better drone spacing
    start_angle = np.pi / 4
    end_angle = 7 * np.pi / 4
    angles = np.linspace(start_angle, end_angle, 9)  # fixed number of drones

    positions = []

    for theta in angles:
        x_coordinate = 0
        y_coordinate = y_offset + 0.1 + radius * np.cos(theta) # added 0.1 to compensate for increased radius
        z_coordinate = z_height + 1 + radius * np.sin(theta)
        positions.append([x_coordinate, y_coordinate, z_coordinate])

    return positions


def D_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'D' formation using 12 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'D' formation.
    """
    drone_box_size = 0.4
    spine_count = 6
    total_drones = 12
    arc_count = total_drones - spine_count

    # Vertical spine (left side)
    spine_positions = [
        (0, y_offset - 0.8, i * (2 / (spine_count - 1)) + z_height)
        for i in range(spine_count)
    ]

    # Arc (right side)
    arc_positions = []
    last_pos = None
    min_dist = drone_box_size * 1.05
    angels = np.linspace(np.pi/2, -np.pi/2, arc_count)

    for angle in angels:
        radius = 1
        x_coordinate = 0
        y_coordinate = y_offset + radius * np.cos(angle)
        z_coordinate = z_height + 1 + radius * np.sin(angle)
        pos = np.array([x_coordinate, y_coordinate, z_coordinate])
        if last_pos is None or np.linalg.norm(pos - last_pos) >= min_dist:
            arc_positions.append(tuple(pos))
            last_pos = pos
        if len(arc_positions) == arc_count:
            break

    positions = spine_positions + arc_positions

    return positions


def E_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'E' formation using 11 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'E' formation.
    """
    positions = []
    vertical_spacing = 1/2

    # Vertical spine (5 drones)
    spine_z = [z_height + i * vertical_spacing for i in range(5)]
    for z in spine_z:
        positions.append((0, y_offset - 0.8, z))  

    # Bottom horizontal
    z_bottom = z_height
    positions.append((0, y_offset - 0, z_bottom))
    positions.append((0, y_offset + 0.8, z_bottom))

    # Middle horizontal
    z_middle = z_height + vertical_spacing * 2
    positions.append((0, y_offset - 0, z_middle))
    positions.append((0, y_offset + 0.8, z_middle))

    # Top horizontal
    z_top = z_height + vertical_spacing * 4
    positions.append((0, y_offset - 0, z_top))
    positions.append((0, y_offset + 0.8, z_top))

    return positions


def F_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'F' formation using 9 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'F' formation.
    """
    positions = []
    vertical_spacing = 1/2

    # Vertical spine (5 drones)
    spine_z = [z_height + i * vertical_spacing for i in range(5)]
    for z in spine_z:
        positions.append((0, y_offset - 0.9, z))

    # Top bar
    z_top = z_height + vertical_spacing * 4
    positions.append((0, y_offset - 0.1, z_top))
    positions.append((0, y_offset + 0.9, z_top))

    # Middle bar
    z_middle = z_height + vertical_spacing * 2
    positions.append((0, y_offset - 0.1, z_middle))
    positions.append((0, y_offset + 0.7, z_middle))

    return positions


def G_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'G' formation using 11 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'G' formation.
    """
    positions = []
    radius = 1 
    angles = np.linspace(np.pi / 4, 3 * np.pi / 2, 7)

    # Circle segment (arc of the 'G')
    for angle in angles:
        x_coordinate = 0
        y_coordinate = y_offset + radius * np.cos(angle)
        z_coordinate = z_height + 1 + radius * np.sin(angle) 
        positions.append((x_coordinate, y_coordinate, z_coordinate))
    
    # Horizontal segment (two points along y-axis)
    for i in range(2):
        x_coordinate = 0
        y_coordinate = y_offset + 0.8
        z_coordinate = z_height + i * 0.4
        positions.append((x_coordinate, y_coordinate, z_coordinate))
    
    # Vertical segment (two points along z-axis)
    for i in range(2):
        x_coordinate = 0
        y_coordinate = y_offset + 0.8 - (i * 0.6)
        z_coordinate = z_height + 0.8
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def H_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'H' formation using 12 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'H' formation.
    """
    positions = []
    vertical_spacing = 1/2

    # Left leg
    for i in range(5):
        x_coordinate = 0
        y_coordinate = y_offset - 1.0
        z_coordinate = z_height + 2 - i * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Right leg
    for i in range(5):
        x_coordinate = 0
        y_coordinate = y_offset + 1.0
        z_coordinate = z_height + 2 - i * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Middle bar (just one drone in the center)
    for i in range(2):
        x_coordinate = 0
        y_coordinate = y_offset - 0.3 + i * 0.6
        z_coordinate = z_height + 1
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def I_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'I' formation using 9 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'I' formation.
    """
    positions = []

    horizontal_length = 1.7
    vertical_spacing = 0.5
    x_coordinate = 0

    # Top bar (3 drones)
    y_top = np.linspace(y_offset - horizontal_length / 2, y_offset + horizontal_length / 2, 3)
    for y_coordinate in y_top:
        z_coordinate = z_height + vertical_spacing * 4
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    for i in range(1, 4):
        x_coordinate = 0
        y_coordinate = y_offset
        z_coordinate = z_height + i * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Bottom bar (3 drones)
    y_bottom = np.linspace(y_offset - horizontal_length / 2, y_offset + horizontal_length / 2, 3)
    for y_coordinate in y_bottom:
        z_coordinate = z_height
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def J_formation_vertical(z_height, y_offset):
    """
    Generates a proportional vertical 'J' formation using 12 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'J' formation.
    """
    # Division of the drones
    vertical_line = 3
    top_line = 3
    bottom_curve = 6

    positions = []

     # Vertical line on the right
    for i in range(vertical_line):
        x_coordinate = 0
        y_coordinate = 1.0
        z_coordinate = z_height + 2.0 - (i * (9/20))
        positions.append((x_coordinate, y_coordinate + y_offset, z_coordinate))

    # Top horizontal line (from right to left)
    for i in range(top_line):
        x_coordinate = 0
        y_coordinate = y_offset + 0.4 - (i * 0.6)
        z_coordinate = z_height + 2.0
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Lower curved hook (J-shape)
    # Arc from the lower right position to the left and upwards
    for i in range(bottom_curve):
        # Parametric curve for the J-hook
        angle = (i / (bottom_curve - 1)) * np.pi
        vertical_compression_factor = 2/3

        # Adjust radius and center of the arc
        radius = 1 # Size of the J-hook
        center_z = z_height + 0.65  # Center of the arc

        x_coordinate = 0
        y_coordinate = y_offset + radius * np.cos(angle + np.pi)
        z_coordinate = center_z + radius * np.sin(angle + np.pi) * vertical_compression_factor  # The + π shifts the start point by 180° so the hook points the right way
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def K_formation_vertical(z_height, y_offset):
    """
    Generates a proportional vertical 'K' formation using 12 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'K' formation.
    """
    positions = []

    # Set drone distribution
    spine_count = 5
    upper_diag_count = 4
    lower_diag_count =4

    # Vertical spine (left side)
    for i in range(spine_count):
        x_coordinate = 0
        y_coordinate = y_offset - 1.0
        z_coordinate = z_height + i * 0.5
        positions.append((x_coordinate, y_coordinate+0.16, z_coordinate))

    # Upper diagonal (from middle to upper right)
    for i in range(1,upper_diag_count):
        vertical_spacing = i / (upper_diag_count - 1) if upper_diag_count > 1 else 0
        x_coordinate = 0
        y_coordinate = y_offset - 0.2 + vertical_spacing * 1.2
        z_coordinate = z_height + 1.0 + vertical_spacing * 1.0
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Lower diagonal (from middle to lower right)
    for i in range(lower_diag_count):
        vertical_spacing = i / (lower_diag_count - 1) if lower_diag_count > 1 else 0
        x_coordinate = 0
        y_coordinate = y_offset - 0.2 + vertical_spacing * 1.2
        z_coordinate = z_height + 1.0 - vertical_spacing * 1.0
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def L_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'L' formation using 7 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'L' formation.
    """
    positions = []

    # Vertical spine (left side)
    for i in range(5):
        x_coordinate = 0
        y_coordinate = y_offset - 0.8
        z_coordinate = z_height + i * 0.5
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Bottom horizontal line
    for i in range(2):
        x_coordinate = 0
        y_coordinate = y_offset - 0.8 + i * 0.9 + 0.7
        z_coordinate = z_height
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def M_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'M' formation using 13 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'M' formation.
    """
    positions = []

    # Left spine (excluding top)
    for i in range(5):
        vertical_spacing = 2 / (5 - 1)
        x_coordinate = 0
        y_coordinate = y_offset - 1.0
        z_coordinate = z_height + i * vertical_spacing
        positions.append((x_coordinate, y_coordinate-0.1, z_coordinate))

    # Left diagonal
    for i in range(1,2):  # skip i=0
        vertical_spacing = i / 2
        x_coordinate = 0
        y_coordinate = y_offset - 1.0 + vertical_spacing
        z_coordinate = z_height + vertical_spacing * 3
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Right diagonal
    for i in range(0,2):
        vertical_spacing = 0.5
        steps = i / 2
        x_coordinate = 0
        y_coordinate = y_offset + steps
        z_coordinate = z_height + vertical_spacing * 2 + steps * vertical_spacing * 2
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Right spine (excluding top)
    for i in range(5):
        vertical_spacing = 0.5
        x_coordinate = 0
        y_coordinate = y_offset + 1.0
        z_coordinate = z_height + vertical_spacing * 4 - i * vertical_spacing
        positions.append((x_coordinate, y_coordinate+0.1, z_coordinate))

    return positions


def N_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'N' formation using 11 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'N' formation.
    """
    positions = []
    vertical_spacing = 2/3

    # Left spine
    for i in range(4):
        x_coordinate = 0
        y_coordinate = y_offset - 1.0
        z_coordinate = z_height + i * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Diagonal from bottom left to top right
    for i in range(1,4):
        steps = i / 4  # 5 drones, 4 steps
        x_coordinate = 0
        y_coordinate = y_offset - 1.0 + steps * 2
        z_coordinate = z_height + vertical_spacing * 3 - steps * vertical_spacing * 3
        positions.append((x_coordinate, y_coordinate, z_coordinate))


    # Right spine
    for i in range(4):
        x_coordinate = 0
        y_coordinate = y_offset + 1.0
        z_coordinate = z_height + i * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def O_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'O' formation using 10 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'O' formation.
    """
    n_drones = 10
    positions = []
    angles = np.linspace(0, 2 * np.pi, n_drones, endpoint=False)
    radius = 1.05
    center_y = y_offset
    center_z = z_height + 1.0

    for angle in angles:
        x_coordinate = 0
        y_coordinate = center_y + radius * np.cos(angle)
        z_coordinate = center_z + radius * np.sin(angle)
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def P_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'P' formation using 11 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'P' formation.
    """
    positions = []

    # Parameters
    spine_count = 5
    arc_count = 6
    radius_y = 0.8
    radius_z = 0.6
    vertical_spacing = 0.5

    # Vertical spine (left side)
    for i in range(spine_count):
        x_coordinate = 0
        y_coordinate = y_offset - 0.9
        z_coordinate = z_height + 2 - i * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Arc (top right semi-circle)
    center_y = y_offset - 1.0 + radius_y
    center_z = z_height + vertical_spacing * 4 - radius_z
    angles = np.linspace(np.pi / 2, -np.pi / 2, arc_count)

    for angle in angles:
        x_coordinate = 0
        y_coordinate = center_y + radius_y * np.cos(angle) * 1.5
        z_coordinate = center_z + radius_z * np.sin(angle)
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def Q_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'Q' formation using 14 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'Q' formation.
    """
    positions = []
    n=15
    circle_count = int(n * 0.85)
    tail_count = n - circle_count

    # Circle part
    angles = np.linspace(0, 2 * np.pi, circle_count, endpoint=False)
    radius = 1.0
    center_y = y_offset
    center_z = z_height + 1.0

    for angle in angles:
        x_coordinate = 0
        y_coordinate = center_y + radius * np.cos(angle)
        z_coordinate = center_z + radius * np.sin(angle)
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Tail (short diagonal line from bottom right)
    tail_length = 1.0  # total tail length to stretch spacing
    tail_positions = []
    for i in range(tail_count):
        vertical_spacing  = i / max(tail_count - 1, 1)
        x_coordinate = 0
        y_coordinate = y_offset + 0.5 + vertical_spacing  * tail_length -0.3
        z_coordinate = z_height + 0.5 - vertical_spacing  * tail_length +0.3
        tail_positions.append((x_coordinate, y_coordinate, z_coordinate))

    if len(tail_positions) > 2:
        middle = len(tail_positions) // 2
        del tail_positions[middle]

    positions.extend(tail_positions)

    return positions


def R_formation_vertical(z_height, y_offset):
    """
    Generates a proportional vertical 'R' formation using 14 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'R' formation.
    """
    positions = []

    # Left vertical line with 6 points, z decreases linearly
    for i in range(6):
        x_coordinate = 0
        y_coordinate = y_offset - 0.75
        z_coordinate = z_height + 2 - (2/5 * i)
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Middle vertical line for the circle with 2 points, z decreases by 1 each step
    for i in range(2):
        x_coordinate = 0
        y_coordinate = y_offset - 0.15
        z_coordinate = z_height + 2 - i
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Circular arrangement with 3 points, y alternates by 0.3, z decreases by 0.4 each step
    for i in range(3):
        x_coordinate = 0
        y_coordinate = y_offset + 0.45  + (i % 2) * 0.3
        z_coordinate = z_height + 1.9 - (0.4 * i)
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Right leg with 3 points, y increases gradually by 0.25 + i/4, z decreases by 3/8 each step
    for i in range(3):
        x_coordinate = 0
        y_coordinate = y_offset + 0.25 + i/4
        z_coordinate = z_height + 0.75 - (3/8 * i)
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def S_formation_vertical(z_height, y_offset):
    """
    Generates a proportional vertical 'S' formation using 13 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'S' formation.
    """
    positions = []
    top_drones = 5
    middle_drones = 3
    bottom_drones = 5

    for i in range(top_drones):
        angle = np.pi - (i * np.pi / (top_drones - 1))
        x_coordinate = 0
        y_coordinate = -1 * (1 * np.cos(angle)) + y_offset
        z_coordinate = 0.5 * np.sin(angle) + 1.5 + z_height
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    for i in range(middle_drones):
        vertical_spacing = (i - 1)/2
        x_coordinate = 0
        y_coordinate = y_offset + vertical_spacing
        z_coordinate = z_height + 1 - vertical_spacing/2
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    for i in range(bottom_drones):
        angle = np.pi - (i * np.pi / (bottom_drones - 1))
        x_coordinate = 0
        y_coordinate = 1 * np.cos(angle) + y_offset
        z_coordinate = -0.5 * np.sin(angle) + 0.5 + z_height
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def T_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'T' formation using 7 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'T' formation.
    """
    positions = []
    horizontal_spacing = 2/3
    vertical_spacing = 0.5

    # Oberer Querbalken (3 Drohnen)
    start_y = y_offset - 1
    z_top = z_height + vertical_spacing * 4  # ganz oben
    for i in range(4):
        x_coordinate = 0
        y_coordinate = start_y + i * horizontal_spacing
        z_coordinate = z_top
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Vertikale Linie darunter (4 Drohnen unter dem mittleren Punkt)
    for i in range(4):
        x_coordinate = 0
        y_coordinate = y_offset
        z_coordinate = z_top - (i + 1) * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions

    
def U_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'U' formation using 9 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'U' formation.
    """
    positions = []
    vertical_spacing = 0.5
    arc_radius = 1.0

    # Left vertical side
    for i in range(2):
        x_coordinate = 0
        y_coordinate = y_offset - 1.0
        z_coordinate = z_height + (2 - i) * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate+1))

    # Bottom arc (semi-circle)
    arc_angles = np.linspace(np.pi, 2 * np.pi, 5)
    for angle in (arc_angles):
        x_coordinate = 0
        y_coordinate = y_offset + arc_radius * np.cos(angle)
        z_coordinate = z_height + arc_radius * np.sin(angle)
        positions.append((x_coordinate, y_coordinate, z_coordinate+1))

    # Right vertical side
    for i in range(2):
        x_coordinate = 0
        y_coordinate = y_offset + 1.0
        z_coordinate = z_height + (2 - i) * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate+1))

    return positions


def V_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'V' formation using 7 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'V' formation.
    """
    positions = []
    count_per_side = 4

    # Left arm
    for i in range(count_per_side):
        vertical_spacing = i / (count_per_side - 1)
        x_coordinate = 0
        y_coordinate = y_offset - 1 + vertical_spacing
        z_coordinate = z_height + 2 - 2 * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Right arm
    for i in range(count_per_side-1):
        vertical_spacing = i / (count_per_side - 1)
        x_coordinate = 0
        y_coordinate = y_offset + 1 - vertical_spacing
        z_coordinate = z_height + 2 - 2 * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def W_formation_vertical(z_height=0, y_offset=0):
    # drone number: 13
    """
    Generates a proportional vertical 'W' formation using 13 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'W' formation.
    """
    positions = []
    vertical_spacing = 0.5

    # Left spine (excluding top)
    for i in range(5):
        x_coordinate = 0
        y_coordinate = y_offset - 1.0
        z_coordinate = z_height + i * vertical_spacing
        positions.append((x_coordinate, y_coordinate-0.1, z_coordinate))

    # Left diagonal
    for i in range(1,2):  # skip i=0
        x_coordinate = 0
        y_coordinate = y_offset - i / 2
        z_coordinate = z_height + i * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Right diagonal
    for i in range(0,2):
        x_coordinate = 0
        y_coordinate = y_offset + i / 2
        z_coordinate = z_height - i * vertical_spacing + 1
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Right spine (excluding top)
    for i in range(5):
        x_coordinate = 0
        y_coordinate = y_offset + 1.0
        z_coordinate = z_height + i * vertical_spacing
        positions.append((x_coordinate, y_coordinate+0.1, z_coordinate))

    return positions


def X_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'X' formation using 9 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'X' formation.
    """
    positions = []
    count = 5

    # Top-left to bottom-right diagonal
    for i in range(count):
        if i == count // 2:  # skip the middle drone
            continue
        vertical_spacing = i / (count - 1)
        x_coordinate = 0
        y_coordinate = y_offset - 1 + 2 * vertical_spacing
        z_coordinate = z_height + 2 - 2 * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Bottom-left to top-right diagonal
    for i in range(count):
        vertical_spacing = i / (count - 1)
        x_coordinate = 0
        y_coordinate = y_offset - 1 + 2 * vertical_spacing
        z_coordinate = z_height + 2 * vertical_spacing
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def Y_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'Y' formation using 9 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'Y' formation.
    """
    positions = []
    arm_length = 3
    spine_length = 3

    # Linker Arm: x = -0.15
    for i in range(arm_length):
        vertical_spacing = i / (arm_length - 1)
        x_coordinate = 0
        y_coordinate = round(y_offset - 1 + vertical_spacing * 0.7, 3)       # von -1 nach -0.3
        z_coordinate = round(z_height + 2 - vertical_spacing * 0.7, 3)  # von 2 nach 1.3
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Rechter Arm: x = 0.15
    for i in range(arm_length):
        vertical_spacing = i / (arm_length - 1)
        x_coordinate = 0
        y_coordinate = round(y_offset + 1 - vertical_spacing * 0.7, 3)       # von +1 nach +0.3
        z_coordinate = round(z_height + 2 - vertical_spacing * 0.7, 3)
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Vertikale Mitte: x = 0.0, y = 0.0, z gestreckt
    for i in range(spine_length):
        vertical_spacing = 0.5
        x_coordinate = 0
        y_coordinate = round(y_offset, 3)
        z_coordinate = round(z_height + 1.0 - i * vertical_spacing, 3)
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def Z_formation_vertical(z_height=0, y_offset=0):
    """
    Generates a proportional vertical 'Z' formation using 11 drones.

    Parameters:
        z_height (float): Height (z-coordinate) at which the drones are positioned.
        y_offset (float): Lateral offset added to the y-coordinate of all drones.

    Returns:
        list of tuple: List of (x, y, z) coordinates representing drone positions in the 'Z' formation.
    """
    positions = []

    # Define section sizes manually for best shape
    top_count = 4
    diag_count = 5
    bottom_count = 4

    # Top horizontal line
    for i in range(top_count-1):
        horizontal_spacing  = i / (top_count - 1) if top_count > 1 else 0
        y_coordinate = y_offset - 1 + horizontal_spacing  * 2
        z_coordinate = z_height + 2
        positions.append((0, y_coordinate, z_coordinate))

    # Diagonal from top-right to bottom-left
    for i in range(diag_count):
        vertical_spacing  = i / (diag_count - 1) if diag_count > 1 else 0
        x_coordinate = 0
        y_coordinate = y_offset + 1 - vertical_spacing * 2
        z_coordinate = z_height + 2 - vertical_spacing * 2
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    # Bottom horizontal line
    for i in range(1,bottom_count):
        horizontal_spacing  = i / (top_count - 1) if top_count > 1 else 0
        x_coordinate = 0
        y_coordinate = y_offset - 1 + horizontal_spacing  * 2
        z_coordinate = z_height 
        positions.append((x_coordinate, y_coordinate, z_coordinate))

    return positions


def space_formation_vertical(z_height, y_offset):
    """
    Function to create a space between letters in the formation.

    Parameters:
        z_height (float): Vertical offset (not used).
        y_offset (float): Horizontal offset (not used).

    Returns:
        list of tuple: Empty list indicating no drone positions.
    """
    return []

char_to_function = {

    'A': A_formation_vertical,
    'B': B_formation_vertical,
    'C' : C_formation_vertical,
    'D' : D_formation_vertical,
    'E' : E_formation_vertical,
    'F' : F_formation_vertical,
    'G' : G_formation_vertical,
    'H' : H_formation_vertical,
    'I' : I_formation_vertical,
    'J' : J_formation_vertical,
    'K' : K_formation_vertical,
    'L' : L_formation_vertical,
    'M' : M_formation_vertical,
    'N' : N_formation_vertical,
    'O' : O_formation_vertical,
    'P' : P_formation_vertical,
    'Q' : Q_formation_vertical,
    'R' : R_formation_vertical,
    'S' : S_formation_vertical,
    'T' : T_formation_vertical,
    'U' : U_formation_vertical,
    'V' : V_formation_vertical,
    'W' : W_formation_vertical,
    'X' : X_formation_vertical,
    'Y' : Y_formation_vertical,
    'Z' : Z_formation_vertical,
    ' ' : space_formation_vertical

}

positions = G_formation_vertical(z_height=0.5, y_offset=0) 
