"""
Dal post:
http://a-ma.us/wp/2012/04/multidimensional-scaling/
"""
from numpy import *
import scipy.linalg


def metric(x, y):
    """
    Compute the pairwise distance between vector x and y
    """
    d = 2
    summ = []
    i = 0
    while i < len(x):
        # in this case use euclidean distance
        summ.append((x[i] - y[i])**d)
        i = i + 1
    return sum(summ) ** (1 / float(d))


def pairwise_distances(data):
    """
    Calcolo matrice delle distanze,
    a partire dalla matrice delle posizioni dei partiti
    """
    distances = []
    for x in data:
        distances_row = []
        for y in data:
            distances_row.append(metric(x, y)**2)
        distances.append(distances_row)
    return distances


def normalize_coords(coords):
    """
    Normalize all coords, so that the range of the values are between 0 and 1
    Coordinates, have 3 significative digits.
    """
    # minimax a-la-python
    (max_x, max_y) = map(max, zip(*coords))[1:3]
    (min_x, min_y) = map(min, zip(*coords))[1:3]

    x_range = max_x - min_x
    y_range = max_y - min_y
    #print 'coords:', coords
    norm_coords = map(lambda x: [x[0],
                                 "%.8f" % ((x[1]-min_x)/x_range),
                                 "%.8f" % ((x[2]-min_y)/y_range)], coords)
    return norm_coords


def centering_matrix(n):
    """
    Construct an n x n centering matrix
    The form is P = I - (1/n) U where U is a matrix of all ones
    """
    P = eye(n) - 1/float(n) * ones((n,n))
    return P


def execute(entities, values_dict):
#    print
#    print 'execute'
#    print 'entities',entities
#    print 'values_dict', values_dict

    # costruisce matrice delle distanze
    X = pairwise_distances(values_dict)

    P = centering_matrix(len(entities))
    A = -1/2.0 * P * X * P
    [vals, vectors] = scipy.linalg.eig(A)

    coords = []
    for i, v in enumerate(vals):
        v_coords = [entities[i],
                    float(vals[2] * vectors[i][2]),
                    float(vals[1] * vectors[i][1])
        ]
        coords.append(v_coords)

    norm_coords = normalize_coords(coords)

    return norm_coords