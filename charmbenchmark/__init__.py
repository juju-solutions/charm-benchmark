import charms.benchmark
import warnings

class Benchmark(charms.benchmark.Benchmark):
    """
    This module is DEPRECATED. Please use charms.benchmark instead.
    """

    def __init__(self, benchmarks=None):
        warnings.warn("The charm-benchmark library has been renamed charms.benchmark. Please update your code accordingly or report a bug with the upstream project.", DeprecationWarning)
        super(Benchmark, self).__init__(benchmarks)
