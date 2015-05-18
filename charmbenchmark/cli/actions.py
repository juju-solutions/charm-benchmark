#!/usr/bin/env python
import argparse
from charmbenchmark import Benchmark

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


def main():

    if args.benchmarks:
        print args.benchmarks
        Benchmark(args.benchmarks)
    return True


if __name__ == "__main__":
    main()
