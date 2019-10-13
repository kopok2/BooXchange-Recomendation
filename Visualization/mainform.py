"""Form module.

Define form methods to add behavior.
"""

import numpy as np
from sklearn.decomposition import PCA
from engine import load_data, ranking, get_recommendations
from dahakianapi.forms import Form
from dahakianapi.singleton import Singleton



@Singleton
class mainform(Form):
    def load_graph(self):
        k = 10
        X = load_data("buy_data.csv")
        users = []
        user_ids = []
        for key, val in X.items():
            user_ids.append(key)
            user = [0] * 500
            for x in list(val):
                user[x] = 1
            users.append(user)
        sparse_users = np.array(users)
        pca = PCA(n_components=2)
        graph_users = pca.fit_transform(sparse_users)
        user_points = []
        edges = []

        vis_x_size = 1700
        vis_y_size = 980
        lib_size = 500

        for x in range(len(user_ids)):
            user_points.append({'id': user_ids[x], 'point': graph_users[x, :].tolist()})

        # preparing points for visualization
        mnx, mny = 1000, 1000
        mxx, mxy = 0, 0
        for u in user_points:
            mnx = min(mnx, u['point'][0])
            mny = min(mny, u['point'][1])
            mxx = max(mxx, u['point'][0])
            mxy = max(mxy, u['point'][1])
        print(mnx, mxx, mny, mxy)

        # normalizing points for visualization

        margin = 50
        dist_x = mxx - mnx
        dist_y = mxy - mny
        for u in user_points:
            u['point'][0] = int(((u['point'][0] - mnx) / dist_x) * vis_x_size) + margin
            u['point'][1] = int(((u['point'][1] - mny) / dist_y) * vis_y_size) + margin

        """
        for x in range(len(user_ids)):
            for book in list(X[user_ids[x]]):
                edges.append({'from': user_points[x],
                              'to': {'id': book, 'point': [int((book / lib_size) * vis_x_size), vis_y_size]},
                              'link': 1.0})
                print(edges[-1])"""

        for x in range(len(user_ids)):
            ranks = ranking(user_ids[x], X, k)
            for voter in ranks:
                vote_power = 1 / (1 + voter[1])
                edges.append({'from': user_points[x],
                              'to': user_points[user_ids.index(voter[0])],
                              'link': vote_power})

        graph = {'points': user_points, 'edges': edges}
        draw_neural(graph)


if __name__ == '__main__':
    localform = mainform('mainform')
    localform.run()
