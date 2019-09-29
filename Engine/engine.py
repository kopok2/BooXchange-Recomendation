# coding=utf-8
"""Collaborative filtering engine for BooXchange E-commerce platform."""

from neighbour_selector import k_ranking


def load_data(in_path="in.csv"):
    """Load data obtained from server.

    Args:
        in_path: file path on server.
    """
    in_ = open(in_path).read().split("\n")
    trans_list = [[int(y) for y in x.split(",")] for x in in_]
    users = {}
    for trans in trans_list:
        if trans[0] in users:
            users[trans[0]].add(trans[1])
        else:
            users[trans[0]] = {trans[1]}
    return users


def ranking(user, user_list, k):
    """Create nearest neighbours ranking for given user using user_list.

    Args:
        user: user Id.
        user_list: list of user datapoints.
        k: number of returned users.

    Returns:
        user ids of k nearest neighbours.
    """
    user_obj = user_list[user]
    ul = [[key, value] for key, value in user_list.items() if key != user]
    ids = k_ranking(ul, k, user_obj)
    return ids


if __name__ == '__main__':
    X = load_data()
    print(ranking(54, X, 3))

