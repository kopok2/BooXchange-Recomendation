# coding=utf-8
"""Collaborative filtering engine for BooXchange E-commerce platform."""

from operator import itemgetter
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


def get_recommendations(user, k, n):
    """Get recommendations for user with given user id.

    Args:
        user: user id.
        k: number of nearest neighbours.
        n: number of suggested products.

    Returns:
        list of book id's with highest ranking.
    """
    # create user ranking
    x_data = load_data()
    ranks = ranking(user, x_data, k)

    # vote for recommendations
    voting = {}
    for voter in ranks:
        vote_power = 1 / (1 + voter[1])
        for book in list(x_data[voter[0]]):
            if book in voting:
                voting[book] += vote_power
            else:
                voting[book] = vote_power

    # filter out already ordered products
    for included in list(x_data[user]):
        del voting[included]

    # get n recommendations
    recomm = [[key, value] for key, value in voting.items()]
    recomm.sort(key=itemgetter(1), reverse=True)

    return [x[0] for x in recomm[:n]]


if __name__ == '__main__':
    print(get_recommendations(54, 10, 4))
