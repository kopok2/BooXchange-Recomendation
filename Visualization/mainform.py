"""Form module.

Define form methods to add behavior.
"""

import pandas as pd
from dahakianapi.forms import Form
from dahakianapi.singleton import Singleton



@Singleton
class mainform(Form):
    def load_graph(self):
        X = pd.read_csv("data.csv")
        print(X)
        draw_neural()


if __name__ == '__main__':
    localform = mainform('mainform')
    localform.run()
