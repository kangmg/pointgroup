import warnings

import numpy as np
from pointgroup.element_data import element_mass


def get_mass(symbols):
    mass_vector = []
    for symbol in symbols:
        try:
            mass_vector.append(element_mass(symbol))
        except KeyError as e:
            warnings.warn('Atomic mass of element {} not found, using 1 u'.format(e))
            mass_vector.append(1.0)
    return mass_vector


def get_center_mass(symbols, coordinates):
    mass_vector = get_mass(symbols)
    cbye = [np.dot(mass_vector[i], coordinates[i]) for i in range(len(symbols))]
    r = np.sum(cbye, axis=0)
    r = r / np.sum(mass_vector)
    return r


def get_inertia_tensor(elements, coord):
    mass_vector = get_mass(elements)

    # Build inertia tensor
    inertia_matrix = np.zeros((3, 3))
    for m, c in zip(mass_vector, coord):
        inertia_matrix += m * (np.identity(3) * np.dot(c, c) - np.outer(c, c))

    total_inertia = 0
    for idx, atom in enumerate(coord):
        total_inertia += mass_vector[idx] * np.dot(atom, atom)

    inertia_matrix /= total_inertia
    return inertia_matrix


def get_perpendicular(vector):
    index = np.argmin(vector)
    p_vector = np.array([0, 0, 0])
    p_vector[index] = 1
    return np.cross(vector, p_vector)/np.linalg.norm(np.cross(vector, p_vector))


def get_degeneracy(eigenvalues, tolerance=0.1):

    for ev1 in eigenvalues:
        single_deg = 0
        for ev2 in eigenvalues:
            if abs(ev1 - ev2) < tolerance:
                single_deg += 1
        if single_deg > 1:
            return single_deg
    return 1


def get_non_degenerated(eigenvalues, tolerance=0.1):

    for i, ev1 in enumerate(eigenvalues):
        single_deg = 0
        index = 0
        for ev2 in eigenvalues:
            if not abs(ev1 - ev2) < tolerance:
                single_deg += 1
                index = i
        if single_deg == 2:
            return index

    raise Exception('Non degenerate not found')