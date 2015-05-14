#!/usr/bin/env python
import argparse
from charmbenchmark import Benchmark

parser = argparse.ArgumentParser(
    description='Set the composite result of a benchmark run.'
)
parser.add_argument(
    "composite",
    metavar='composite',
    # nargs='+',
    help='The composite score of the benchmark run.'
)
parser.add_argument(
    "units",
    metavar='units',
    # nargs='+',
    help='The type of units used to measure the composite, i.e., requests/sec.'
)
parser.add_argument(
    "direction",
    metavar='direction',
    # nargs='+',
    help='''
    The direction of how the composite should be interpreted. 'asc' if a lower
    number is better; 'desc' if a higher number is better.
    '''
)

args = parser.parse_args()


def main():
    Benchmark().set_composite_score(args.composite, args.units, args.direction)
    return True


if __name__ == "__main__":
    main()
