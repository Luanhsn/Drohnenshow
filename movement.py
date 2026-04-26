import numpy as np
import pybullet as p

def interpolate(current_location, target_location, step_size):
    """
    Move the current position towards the target position by a maximum step size.

    Parameters:
        current (array-like): Current position of the drone.
        target (array-like): Destination position to move towards.
        step_size (float): Maximum distance to move in this step.

    Returns:
        numpy.ndarray: New position after moving towards the target.

    Description:
        Calculates the direction vector from current to target and moves the position
        by at most step_size in that direction. If the distance to the target is less
        than step_size, returns the target position directly.
    """
    import numpy as np
    current_location = np.array(current_location)
    target_location = np.array(target_location)
    direction = target_location - current_location
    dist = np.linalg.norm(direction)
    if dist < step_size:
        return target_location
    return current_location + direction / dist * step_size

def all_reached(drones, targets, threshold=0.05):
    """
    Check if all drones are close enough to their destinations.

    Parameters:
        drones (list): List of drone IDs.
        targets (list): List of destination position vectors.
        threshold (float): Maximum acceptable distance to the destination.

    Returns:
        bool: True if all drones have reached their destinations within the threshold, False otherwise.

    Description:
        Iterates through the list of drones and checks if each drone is within the given threshold distance of its destination.
    """
    for i, drone_id in enumerate(drones):
        pos, _ = p.getBasePositionAndOrientation(drone_id)
        if np.linalg.norm(np.array(pos) - np.array(targets[i])) > threshold: # pos, _ means we ignore the orientation
            return False
    return True