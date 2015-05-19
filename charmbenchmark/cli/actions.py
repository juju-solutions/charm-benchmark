#!/usr/bin/env python
import argparse
from charmbenchmark import Benchmark


def main():
    parser = argparse.ArgumentParser(
        description='Inform the Benchmark GUI of available benchmarks'
    )
    parser.add_argument(
        "benchmarks",
        metavar='benchmark(s)',
        nargs='+',
        help='A space-delimited list of benchmarks exposed by the charm.'
    )
    args = parser.parse_args()

    Benchmark(args.benchmarks)


if __name__ == "__main__":
    main()
