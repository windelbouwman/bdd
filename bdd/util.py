""" Utility functions """

import inspect
import os


def rel(filename, back=1):
    """ Return an absolute path relative to the file where this function is
    called from """
    frame = inspect.stack()[back]
    dirname = os.path.dirname(os.path.abspath(frame[1]))
    return os.path.join(dirname, filename)
