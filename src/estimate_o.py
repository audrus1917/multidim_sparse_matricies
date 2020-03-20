#!/usr/bin/env python3

import sys
import random
import time
import argparse

from contextlib import contextmanager

from matplotlib import pyplot as plt

from coo_matrix import CooMatrix, DimensionError

# Default values
DEFAULT_SHAPE_SIZE = 5
DEFAULT_START_SIZE = 10
DEFAULT_TOTAL = 10
DEFAULT_MULTIPLIER = 10
DEFAULT_ACTIONS = 10


def log_error(error_msg):
    """Print the error message to stderr."""
    print(error_msg, file=sys.stderr)


class ActionTimer(object):
    def __enter__(self):
        self.start = time.time()
        self.delta = 0.0
        return self

    def __exit__(self, type, value, traceback):
        self.delta = time.time() - self.start


def main(exe_args):
    x_dimensions, y_reading, y_writing = [], [], []

    current_size = exe_args.start_size
    for _idx in range(exe_args.total):
        current_size = exe_args.start_size * \
            exe_args.multiplier ** _idx
        x_dimensions.append(current_size)
        shape = [current_size for __ in range(exe_args.shape_size)]
        coo_matrix = CooMatrix(shape)

        # writing
        stored = []
        with ActionTimer() as atimer:
            for __ in range(DEFAULT_ACTIONS):
                random_coords = tuple(
                    random.randint(0, coo_matrix.shape[n])
                        for n in range(coo_matrix.dimensions)
                )
                random_value = random.randint(0, 10)
                coo_matrix.update(random_coords, random_value)
                stored.append(random_coords)
        y_writing.append(atimer.delta * 1000000)

        # reading
        with ActionTimer() as atimer:
            for __ in range(DEFAULT_ACTIONS):

                # From stored cell or from random
                if random.choice((True, False)):
                    coords = random.choice(stored)
                else:
                    coords = tuple(
                        random.randint(0, coo_matrix.shape[n])
                            for n in range(coo_matrix.dimensions)
                    )
                coo_matrix.get_value(random_coords)
        y_reading.append(atimer.delta * 1000000)
    
    print('-' * 64)
    print('|{0:^20s}|{1:^20}|{2:^20s}|'\
        .format('Size', 'Writing (mks)', 'Reading (mks)')) 
    print('-' * 64)
    for _idx in range(exe_args.total):
        print(
            '|{0:^20d}|{1:>20.7f}|{2:>20.7f}|'\
                .format(
                    x_dimensions[_idx], 
                    y_writing[_idx],
                    y_reading[_idx]    
                )
        )

    print('-' * 64)

    if exe_args.plot:
        plt.title('Complexity estimation')
        plt.ylabel('Time (mks)')
        plt.xlabel('Matrix dimension')
        plt.xscale('symlog')
        plt.plot(x_dimensions ,y_writing , 'g', label='Writing', linewidth=2)
        plt.plot(x_dimensions, y_reading, 'r', label='Reading', linewidth=2)
        plt.legend()
        plt.grid(True,color='k')
        plt.savefig("estimate.png")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sparse matrix sample')
    parser.add_argument('--start-size', type=int, default=DEFAULT_START_SIZE)
    parser.add_argument('--total', type=int, default=DEFAULT_TOTAL)
    parser.add_argument('--multiplier', type=int, default=DEFAULT_MULTIPLIER)
    parser.add_argument('--shape-size', type=int, default=DEFAULT_SHAPE_SIZE)
    parser.add_argument('--plot', action='store_true')
    exe_args = parser.parse_args()

    try:
        main(exe_args)
    except DimensionError as exc:
        log_error(exc)
        sys.exit(1)