import numpy as np
from scipy.optimize import linear_sum_assignment


def assign_drones_to_targets(drones, targets):
    """
    Ordnet Drohnen so Zielpositionen zu, dass die Gesamtdistanz minimiert wird.
    """
    n = len(drones)
    cost_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            cost_matrix[i, j] = np.linalg.norm(np.array(drones[i]) - np.array(targets[j]))

    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    return [targets[j] for j in col_ind]
