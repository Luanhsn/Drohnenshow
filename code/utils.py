def set_camera(yaw, pitch, distance, target):
    """
    Timeline recording
    """
    import pybullet as p
    p.resetDebugVisualizerCamera(
        cameraDistance=distance,
        cameraYaw=yaw,
        cameraPitch=pitch,
        cameraTargetPosition=target
    )

def select_drawn_points(points, num_out):
    """
    Selects 'num_out' points from the user-drawn points list.
    If there are more points than needed, select evenly spaced points.
    If there are fewer or exactly as many points as needed, use all points (and possibly warn or pad).

    Args:
        points (list or np.ndarray): List of (x, y) or (x, y, z) points.
        num_out (int): Number of output points to generate.

    Returns:
        np.ndarray: Array of shape [num_out, dim] with selected points.
    """
    import numpy as np
    points = np.array(points)
    n = len(points)
    if n == 0:
        raise ValueError("No points provided.")
    if n == num_out:
        # Use all user points as they are
        return points
    elif n > num_out:
        # Select evenly spaced points
        idx = np.linspace(0, n - 1, num_out).astype(int)
        return points[idx]
    else:
        # Fewer points than needed: repeat last point or pad (here: repeat last)
        pad = np.vstack([points, np.tile(points[-1], (num_out - n, 1))])
        return pad 