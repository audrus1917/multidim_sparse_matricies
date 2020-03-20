#!/usr/bin/env python3

import sys
import random
import time
import argparse

from matplotlib import pyplot as plt

from coo_matrix import CooMatrix, DimensionError

# Default values
DEFAULT_SHAPE_SIZE = 5
DEFAULT_START_SIZE = 1000
DEFAULT_TOTAL = 100
DEFAULT_MULTIPLIER = 2


def log_error(error_msg):
    """Print the error message to stderr."""
    print(error_msg, file=sys.stderr)


def main(exe_args):
    xs = []
    y_reading = []
    y_writing = []

    current_size = exe_args.start_size

    for i in range(1, exe_args.total):
        current_size = current_size * (exe_args.multiplier - 1)
        shape = [current_size for __ in range(exe_args.shape_size)]
        coo_matrix = CooMatrix(shape)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sparse matrix sample')
    parser.add_argument('--start-size', type=int, default=DEFAULT_START_SIZE)
    parser.add_argument('--total', type=int, default=DEFAULT_TOTAL)
    parser.add_argument('--multiplier', type=int, default=DEFAULT_MULTIPLIER)
    parser.add_argument('--shape-size', type=int, default=DEFAULT_SHAPE_SIZE)
    exe_args = parser.parse_args()

    try:
        main(exe_args)
    except DimensionError as exc:
        log_error(exc)
        sys.exit(1)