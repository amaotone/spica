import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.neighbors import NearestNeighbors


class NeighborDistance(BaseEstimator, TransformerMixin):
    def __init__(self, n_neighbors, **kwargs):
        self.n_neighbors = n_neighbors
        self.kwargs = kwargs
        super().__init__()

    def fit(self, X, y):
        self.models = {i: NearestNeighbors(n_neighbors=self.n_neighbors, **self.kwargs) for i in np.unique(y)}
        for i in enumerate(np.unique(y)):
            self.models[i].fit(X[y == i])
        return self

    def transform(self, X):
        res = []
        for i, model in sorted(self.models.items()):
            dist, _ = model.kneighbors(X, n_neighbors=self.n_neighbors)
            res.append(dist)
        return np.concatenate(res, axis=1)

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y)
        return self.transform(X)

    def get_params(self, deep=True):
        return {'n_neighbors': self.n_neighbors, 'kwargs': self.kwargs}

    def set_params(self, **params):
        for param, value in params.items():
            setattr(self, param, value)
        return self
