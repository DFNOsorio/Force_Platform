def convert2mass(data_filtered, offsets, resolution):
    mass = []

    for i in range(0, len(offsets)):
        Voutput = float('2.'+'0'*(5-len(str(offsets[i])))+str(offsets[i]))
        G = (100*1000 + 203.83)/203.83
        Vi = 1000.0/G
        S = (3.0 * Voutput)/(Vi * 200.0)

        corner_mass = ((data_filtered[:, i])* 3.0) / (S * (2.0**(resolution) - 1))

        mass.append(corner_mass)

    return mass

def getCops(mass, weightThr, zero_cop):
    COPx = []
    COPy = []
    W = 225+12
    H = 225+12

    TL = mass[0]
    TR = mass[1]
    BR = mass[2]
    BL = mass[3]

    for i in range(0, len(mass[0])):
        total_weight = TL[i] + TR[i] + BR[i] + BL[i]
        if total_weight > weightThr:
            COPx.append((W) * ((TR[i] + BR[i]) - (TL[i] + BL[i])) / (total_weight * 1.0) - zero_cop[0])
            COPy.append((H) * ((TR[i] + TL[i]) - (BR[i] + BL[i])) / (total_weight * 1.0) - zero_cop[1])
        else:
            COPx.append(zero_cop[0])
            COPy.append(zero_cop[1])

    return [COPx, COPy]

def convex_hull(COPx, COPy):
    """Computes the convex hull of a set of 2D points.

    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
    starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """
    points = [(COPx[i], COPy[i]) for i in range(0, len(COPy))]

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list.
    contour = upper[:-1] + lower[:-1] + upper[0:1]

    hull = [list(np.array(contour)[:, 0]), list(np.array(contour)[:, 1])]

    return [hull[0], hull[1]]

def area_calc(contour_array):


    """ This function uses the contour path to calculate the area, using Green's theorem.

    Parameters
    ----------
    contour_array: array
    contour path

    Returns
    -------
    area: float
    value for the area within the contour
    """

    x = contour_array[0]
    y = contour_array[1]
    if min(x)<0:
        x = np.array(x) - min(x)
    if min(y)<0:
        y = np.array(y) - min(y)

    area = 0
    for i in range(1, len(y) - 1):
        area += (y[i - 1] * x[i] - x[i - 1] * y[i])

    area = abs(area) / 2.0
    return area
