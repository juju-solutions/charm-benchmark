#!/usr/bin/env python
import argparse
from charmbenchmark import Benchmark


def main():
    parser = argparse.ArgumentParser(
        description='Set the raw results of a benchmark run.'
    )
    parser.add_argument(
        "value",
        metavar='value',
        help='The raw results of a benchmark run.',
        type=argparse.FileType('r')
    )

    args = parser.parse_args()

    Benchmark.set_data({'meta.raw': args.value.read()})

if __name__ == "__main__":
    main()
