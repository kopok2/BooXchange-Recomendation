# coding=utf-8
"""Distance measures module based on L1/L2 norm calculated on sets."""


def distance(x_1, x_2):
    """Calculate distance between sets.

    Args:
        x_1, x_2: sets.

    Returns:
        distance.
    """
    return len(x_1) + len(x_2) - len(x_1.intersection(x_2)) * 2
