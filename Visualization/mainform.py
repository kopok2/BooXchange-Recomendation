"""Form module.

Define form methods to add behavior.
"""

import csv
import math
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from engine import load_data, ranking, get_recommendations
from dahakianapi.forms import Form
from dahakianapi.singleton import Singleton


def load_book_names():
    reader = csv.reader(open('names.csv', 'r', encoding="utf8"))
    d = {}
    for row in reader:
        k, v = row
        d[k] = v
    # fill unknown books
    for x in range(500):
        if str(x) not in d:
            d[str(x)] = "Book moved"
    return d


@Singleton
class mainform(Form):
    def expand_data(self, perc):
        open("expand.csv", "w").write("\n".join(open("sell_data.csv").readlines()[:perc]))
        self.load_graph(0, 0)

    def load_graph(self, cordx, cordy):
        self.enter_fullscreen()

        # load data
        k = 10
        X = load_data("expand.csv")
        users = []
        user_ids = []
        for key, val in X.items():
            user_ids.append(key)
            user = [0] * 500
            for x in list(val):
                user[x] = 1
            users.append(user)
        sparse_users = np.array(users)

        # dimensionality reduction using scikit-learn
        pca = PCA(n_components=2)
        graph_users = pca.fit_transform(sparse_users)
        clusters = KMeans(n_clusters=7, random_state=0).fit_predict(graph_users)

        # ...
        user_points = []
        edges = []

        vis_x_size = 1500
        vis_y_size = 900
        margin = 50
        selection_margin = 60

        lib_size = 500


        for x in range(len(user_ids)):
            user_points.append({'id': user_ids[x], 'point': graph_users[x, :].tolist(), 'cluster': clusters.tolist()[x]})

        # preparing points for visualization
        mnx, mny = 1000, 1000
        mxx, mxy = 0, 0
        for u in user_points:
            mnx = min(mnx, u['point'][0])
            mny = min(mny, u['point'][1])
            mxx = max(mxx, u['point'][0])
            mxy = max(mxy, u['point'][1])

        # normalizing points for visualization
        dist_x = mxx - mnx
        dist_y = mxy - mny
        for u in user_points:
            u['point'][0] = int(((u['point'][0] - mnx) / dist_x) * vis_x_size) + margin
            u['point'][1] = int(((u['point'][1] - mny) / dist_y) * vis_y_size) + margin

        # choosing selected user
        mn_dist = selection_margin
        chosen_user = 0
        for point in user_points:
            dist = math.sqrt((point['point'][0] - cordx) ** 2 + (point['point'][1] - cordy) ** 2)
            if dist < mn_dist:
                mn_dist = dist
                chosen_user = point['id']

        # plotting selected user basket
        if chosen_user:
            neighbours = [n[0] for n in ranking(chosen_user, X, k)] + [chosen_user]
        else:
            neighbours = []

        books_names = load_book_names()
        used = set()
        for x in range(len(user_ids)):
            if user_ids[x] in neighbours:
                for book in list(X[user_ids[x]]):
                    if book not in used:
                        used.add(book)
                        user_points.append({'id': books_names[str(book)], 'point': [vis_x_size + margin, int((book / lib_size) * vis_y_size)], 'cluster': 0})
                    edges.append({'from': user_points[x],
                                  'to': {'id': book, 'point': [vis_x_size + margin, int((book / lib_size) * vis_y_size)]},
                                  'link': 0.5})

        for x in range(len(user_ids)):
            ranks = ranking(user_ids[x], X, k)
            for voter in ranks:
                vote_power = 1 / (1 + voter[1])
                edges.append({'from': user_points[x],
                              'to': user_points[user_ids.index(voter[0])],
                              'link': vote_power})

        # call js visualization code
        graph = {'points': user_points, 'edges': edges}
        draw_neural(graph)
        print(cordx, cordy)


if __name__ == '__main__':
    localform = mainform('mainform')
    localform.run()
