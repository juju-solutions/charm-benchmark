import os
import unittest
from testtools import TestCase

import mock
from charmbenchmark import Benchmark
from helpers import patch_open, FakeRelation


TO_PATCH = [
    'in_relation_hook',
    'relation_ids',
    'relation_set',
    'relation_get',
]

FAKE_RELATION = {
    'benchmark:0': {
        'benchmark/0': {
            'hostname': '127.0.0.1',
            'port': '1111',
            'graphite_port': '2222',
            'graphite_endpoint': 'http://localhost:3333',
            'api_port': '4444'
        }
    }
}


class TestBenchmark(TestCase):

    def setUp(self):
        super(TestBenchmark, self).setUp()
        for m in TO_PATCH:
            setattr(self, m, self._patch(m))
        self.fake_relation = FakeRelation(FAKE_RELATION)

        self.relation_get.side_effect = self.fake_relation.get
        self.relation_ids.side_effect = self.fake_relation.relation_ids

    def _patch(self, method):
        _m = mock.patch('charmbenchmark.' + method)
        m = _m.start()
        self.addCleanup(_m.stop)
        return m

    def test_foo(self):
        pass

    @mock.patch('charmbenchmark.relation_get')
    @mock.patch('charmbenchmark.relation_set')
    @mock.patch('charmbenchmark.relation_ids')
    @mock.patch('charmbenchmark.in_relation_hook')
    def test_benchmark_init(self, in_relation_hook, relation_ids, relation_set, relation_get):

        in_relation_hook.return_value = True
        relation_ids.return_value = ['benchmark:0']
        actions = ['asdf', 'foobar']

        with patch_open() as (_open, _file):
            b = Benchmark(actions)

            self.assertIsInstance(b, Benchmark)

            self.assertTrue(relation_get.called)
            self.assertTrue(relation_set.called)

            relation_ids.assert_called_once_with('benchmark')

            for key in b.required_keys:
                relation_get.assert_any_call(key)

            relation_set.assert_called_once_with(
                relation_id='benchmark:0',
                relation_settings={'benchmarks': ",".join(actions)}
            )

            # Test benchmark.conf
            _open.assert_called_with('/etc/benchmark.conf', 'w')
            for key, val in iter(FAKE_RELATION['benchmark:0']['benchmark/0'].items()):
                _file.write.assert_any_called("%s=%s\n" % (key, val))

            relation_get.return_value = None
            Benchmark(actions)


    @mock.patch('charmbenchmark.action_set')
    def test_benchmark_start_oserror(self, action_set):
        action_set.side_effect = OSError('File not found')
        self.assertFalse(Benchmark.start())

    @mock.patch('charmbenchmark.action_set')
    def test_benchmark_start_oserror(self, action_set):
        action_set.side_effect = OSError('File not found')
        self.assertFalse(Benchmark.start())

    @mock.patch('charmbenchmark.action_set')
    def test_benchmark_start_oserror(self, action_set):
        action_set.side_effect = OSError('File not found')
        self.assertFalse(Benchmark.start())

    @mock.patch('charmbenchmark.action_set')
    @mock.patch('os.path.exists')
    @mock.patch('subprocess.check_output')
    def test_benchmark_start(self, check_output, exists, action_set):

        exists.return_value = True
        check_output.return_value = "data"
        action_set.return_value = True

        self.assertTrue(Benchmark.start())

        COLLECT_PROFILE_DATA = '/usr/local/bin/collect-profile-data'
        exists.assert_any_call(COLLECT_PROFILE_DATA)
        check_output.assert_any_call([COLLECT_PROFILE_DATA])

    @mock.patch('charmbenchmark.action_set')
    def test_benchmark_finish(self, action_set):
        action_set.return_value = True
        self.assertTrue(Benchmark.finish())

    @mock.patch('charmbenchmark.action_set')
    def test_benchmark_set_composite_score(self, action_set):
        action_set.return_value = True
        self.assertTrue(Benchmark.set_composite_score(15.7, 'hits/sec', 'desc'))
        action_set.assert_called_once_with({'meta.composite': {'value': 15.7, 'units': 'hits/sec', 'direction': 'desc'}})
