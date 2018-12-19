import math

import numpy as np
import pandas as pd
from keras import Input, Model
from keras.layers import Dense
from keras.utils import Sequence


class SwapNoiseGenerator(Sequence):
    def __init__(self, x, y, batch_size, swap_ratio=0.15, shuffle=True):
        self.n_samples, self.n_features = x.shape
        self.x = x.values if isinstance(x, pd.DataFrame) else x
        self.y = y.values if isinstance(y, pd.DataFrame) else x
        self.batch_size = batch_size
        self.swap_ratio = swap_ratio
        self.shuffle = shuffle
        self.indices = np.arange(len(x))
        if self.shuffle:
            self.indices = np.random.permutation(self.indices)

    def __len__(self):
        return math.ceil(self.n_samples / self.batch_size)

    def __getitem__(self, idx):
        indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        x_batch = self.x[indices, :]
        y_batch = self.y[indices, :]
        new_batch = x_batch.copy()
        for i in range(len(x_batch)):
            swap_indices = np.random.choice(self.n_features, int(self.n_features * self.swap_ratio), replace=False)
            new_batch[i, swap_indices] = x_batch[np.random.randint(len(x_batch)), swap_indices]
        return new_batch, y_batch
