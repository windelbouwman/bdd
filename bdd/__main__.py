""" Run bdd """

import argparse
from .runner import Environment, Runner
from .utils import load_features_from_dir


parser = argparse.ArgumentParser()
parser.add_argument('feature_dir')
args = parser.parse_args()

# Load features:
features = load_features_from_dir(args.feature_dir)
env = Environment()

# Run the features:
runner = Runner()
runner.run(features, env)
