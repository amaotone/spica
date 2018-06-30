import argparse
import inspect
import re
from pathlib import Path

import pandas as pd

from .utils import timer


def get_arguments(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--force', '-f', action='store_true', help='Overwrite existing files')
    return parser.parse_args()


def get_features(namespace):
    return inspect.getmembers(namespace, lambda x: inspect.isclass(x) and issubclass(x, Feature))


def generate_features(namespace, overwrite):
    for f in get_features(namespace):
        if f.train_path.exists() and f.test_path.exists() and not overwrite:
            print(f.name, 'was skipped')
        else:
            f.run().save()


class Feature(object):
    prefix = ''
    suffix = ''
    dir = '.'
    
    def __init__(self):
        self.name = re.sub("([A-Z])", lambda x: "_" + x.group(1).lower(), self.__class__.__name__).lstrip('_')
        self.train = pd.DataFrame()
        self.test = pd.DataFrame()
        self.train_path = Path(self.dir) / f'{self.name}_train.ftr'
        self.test_path = Path(self.dir) / f'{self.name}_test.ftr'
    
    def run(self):
        with timer(self.name):
            self.create_features()
            self.train.columns = self.prefix + self.train.columns + self.suffix
            self.test.columns = self.prefix + self.test.columns + self.suffix
        return self
    
    def create_features(self):
        raise NotImplementedError
    
    def save(self):
        self.train.to_feather(str(self.train_path))
        self.test.to_feather(str(self.test_path))
    
    def load(self):
        self.train = pd.read_feather(str(self.train_path))
        self.test = pd.read_feather(str(self.test_path))
