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

    args = parser.parse_args()

    Benchmark.set_meta(args.key, args.value)

if __name__ == "__main__":
    main()
