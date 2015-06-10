#!/usr/bin/env python
import argparse
from charmbenchmark import Benchmark


def main():
    parser = argparse.ArgumentParser(
        description='Set the composite result of a benchmark run.'
    )
    parser.add_argument(
        "key",
        metavar='key',
        help='The key of the data to store, i.e., .'
    )

    parser.add_argument(
        "value",
        metavar='value',
        help='The key of the data to store, i.e., .'
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
        The direction of how the composite should be interpreted. 'asc' if a
        lower number is better; 'desc' if a higher number is better.
        '''
    )

    args = parser.parse_args()

    Benchmark.set_data({'results.%s.value' % args.key: args.value})
    if args.units:
        Benchmark.set_data({'results.%s.units' % args.key: args.units})
    if args.direction:
        Benchmark.set_data({'results.%s.direction' % args.key: args.direction})

if __name__ == "__main__":
    main()
