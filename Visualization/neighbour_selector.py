# coding=utf-8
"""K-Nearest Neighbours selector using L1/L2 norm distance measure."""

from operator import itemgetter
from dist import distance


def k_ranking(user_list, k, point):
    """Get k nearest neigbours to given point.

    Args:
        user_list: user list in form [(user_id, user books set), ...].
        k: number of neighbours to return.
        point: point indicating user position.

    Returns:
        list of k user id's with lowest distance to point.
    """
    distances = [(x[0], distance(x[1], point)) for x in user_list]
    distances.sort(key=itemgetter(1))
    return distances[:k]
