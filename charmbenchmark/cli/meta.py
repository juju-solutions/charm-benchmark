#!/usr/bin/env python
import argparse
from charmbenchmark import Benchmark


def main():
    parser = argparse.ArgumentParser(
        description='Set a meta key of the benchmark run.'
    )
    parser.add_argument(
        "key",
        metavar='key',
        help='The key of the data to store.'
    )

    parser.add_argument(
        "value",
        metavar='value',
        help='The value of the data to store.'
    )

    parser.add_argument(
        "units",
        metavar='units',
        nargs='?',
        help='''
        The type of units used to measure the composite, i.e., requests/sec.
        '''
    )
    parser.add_argument(
        "direction",
        metavar='direction',
        nargs='?',
        help='''
        The direction of how the data should be interpreted. 'asc' if a
        lower number is better; 'desc' if a higher number is better.
        '''
    )

    args = parser.parse_args()

    Benchmark.set_meta(args.key, args.value, args.units, args.direction)

if __name__ == "__main__":
    main()
