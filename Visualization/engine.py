# coding=utf-8
"""Collaborative filtering engine for BooXchange E-commerce platform."""

import sys
from random import randrange
from operator import itemgetter
from neighbour_selector import k_ranking


def load_data(in_path="colab.csv"):
    """Load data obtained from server.

    Args:
        in_path: file path on server.
    """
    try:
        in_ = open(in_path).read().split("\n")
        trans_list = [[int(y.replace('"', "")) for y in x.split(",")[1:3]] for x in in_ if x]
        users = {}
        for trans in trans_list:
            if trans[0] in users:
                users[trans[0]].add(trans[1])
            else:
                users[trans[0]] = {trans[1]}
        return users
    except ValueError:
        return {}


def ranking(user, user_list, k):
    """Create nearest neighbours ranking for given user using user_list.

    Args:
        user: user Id.
        user_list: list of user datapoints.
        k: number of returned users.

    Returns:
        user ids of k nearest neighbours.
    """
    if user in user_list:
        user_obj = user_list[user]
    else:
        user_obj = set()
    ul = [[key, value] for key, value in user_list.items() if key != user]
    ids = k_ranking(ul, k, user_obj)
    return ids


def get_recommendations(user, k, n, data=None):
    """Get recommendations for user with given user id.

    Args:
        user: user id.
        k: number of nearest neighbours.
        n: number of suggested products.

    Returns:
        list of book id's with highest ranking.
    """
    try:
        # create user ranking
        if not data:
            x_data = load_data()
        else:
            x_data = data
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
        if user in x_data:
            for included in list(x_data[user]):
                if included in voting:
                    del voting[included]

        # get n recommendations
        recomm = [[key, value] for key, value in voting.items()]
        recomm.sort(key=itemgetter(1), reverse=True)

        return [x[0] for x in recomm] + [randrange(10, 100) for y in range(max(0, 4 - len(recomm)))]
    except KeyError:
        return []


def server_response(response):
    """Generate response for API usage.

    Args:
        response: object to be returned.

    Returns:
        response in appropriate format.
    """
    return str(response).replace("[", "$to_rec =array(").replace("]", ");")


if __name__ == '__main__':
    k = 10
    n = 4
    user = int(sys.argv[1])
    print(server_response(get_recommendations(user, k, n)))

