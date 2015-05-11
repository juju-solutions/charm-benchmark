import os
import unittest

from mock import patch, MagicMock
from charmbenchmark import Benchmark


class CheckBenchmark(unittest.TestCase):
    @patch('charmhelpers.core.hookenv.action_set')
    @patch('charmbenchmark.Benchmark.start')
    def test_benchmark_start(self, ms, action_set):
        Benchmark.start()
        action_set.assert_called_once()

    @patch('charmhelpers.core.hookenv.action_set')
    @patch('charmbenchmark.Benchmark.finish')
    def test_benchmark_finish(self, ms, action_set):
        Benchmark.finish()
        action_set.assert_called_once()
