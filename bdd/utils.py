""" Utility functions """

import inspect
import os
import glob

from .parser import load_feature


def rel(filename, back=1):
    """ Return an absolute path relative to the file where this function is
    called from """
    frame = inspect.stack()[back]
    dirname = os.path.dirname(os.path.abspath(frame[1]))
    return os.path.join(dirname, filename)


def load_features_from_dir(dirname):
    """ Search for all .feature files in the given directory """
    features = []
    for filename in glob.iglob(
            os.path.join(dirname, '**', '*.feature'), recursive=True):
        features.append(load_feature(filename))
    return features
