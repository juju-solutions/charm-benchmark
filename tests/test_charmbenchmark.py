from testtools import TestCase

import mock
from charmbenchmark import Benchmark

try:
    from exceptions import DeprecationWarning
except:
    # Python 3+ changed how exceptions are handled;
    # no need to import them explicitly
    pass

class TestBenchmark(TestCase):

    def setUp(self):
        super(TestBenchmark, self).setUp()

    def _patch(self, method):
        _m = mock.patch('charmbenchmark.' + method)
        m = _m.start()
        self.addCleanup(_m.stop)
        return m

    @mock.patch('charms.benchmark.Benchmark.__init__')
    @mock.patch('charmbenchmark.warnings.warn')
    def test_benchmark_init(self, warn, init):

        b = Benchmark()
        warn.assert_called_with('The charm-benchmark library has been renamed charms.benchmark. Please update your code accordingly or report a bug with the upstream project.', DeprecationWarning)
        init.assert_called_with(b, None)
