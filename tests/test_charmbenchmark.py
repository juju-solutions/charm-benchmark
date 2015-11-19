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

    @mock.patch('charmbenchmark.action_set')
    def test_set_data(self, action_set):
        action_set.return_value = True
        data = {'key': 'value'}
        self.assertTrue(Benchmark.set_data(data))
        action_set.assert_called_once_with(data)

    @mock.patch('charmbenchmark.relation_get')
    @mock.patch('charmbenchmark.relation_set')
    @mock.patch('charmbenchmark.relation_ids')
    @mock.patch('charmbenchmark.in_relation_hook')
    def test_benchmark_init(self, in_relation_hook, relation_ids,
                            relation_set, relation_get):

        in_relation_hook.return_value = True
        relation_data = FAKE_RELATION['benchmark:0']['benchmark/0']
        relation_ids.return_value = FAKE_RELATION.keys()
        relation_get.side_effect = lambda k: relation_data.get(k)
        actions = ['asdf', 'foobar']

        with patch_open() as (_open, _file):
            b = Benchmark(actions)

            self.assertIsInstance(b, Benchmark)

            relation_ids.assert_called_once_with('benchmark')

            for key in b.required_keys:
                relation_get.assert_any_call(key)

            relation_set.assert_called_once_with(
                relation_id='benchmark:0',
                relation_settings={'benchmarks': ",".join(actions)}
            )

            # Test benchmark.conf
            _open.assert_called_with('/etc/benchmark.conf', 'w')
            for key, val in relation_data.items():
                _file.write.assert_any_call("%s=%s\n" % (key, val))

    @mock.patch('charmbenchmark.action_set')
    def test_benchmark_start_oserror(self, action_set):
        action_set.side_effect = OSError('File not found')
        self.assertFalse(Benchmark.start())

    @mock.patch('charmbenchmark.action_set')
    def test_benchmark_finish_oserror(self, action_set):
        action_set.side_effect = OSError('File not found')
        self.assertFalse(Benchmark.finish())

    @mock.patch.dict('charmbenchmark.os.environ', {
        'JUJU_ACTION_UUID': 'my_action'})
    @mock.patch('charmbenchmark.relation_set')
    @mock.patch('charmbenchmark.relation_ids')
    @mock.patch('charmbenchmark.action_set')
    @mock.patch('os.path.exists')
    @mock.patch('subprocess.check_output')
    def test_benchmark_start(self, check_output, exists, action_set,
                             relation_ids, relation_set):

        exists.return_value = True
        check_output.return_value = "data"
        action_set.return_value = True
        relation_ids.return_value = ['benchmark:1']

        self.assertTrue(Benchmark.start())

        relation_set.assert_called_once_with(
            relation_id='benchmark:1',
            relation_settings={'action_id': 'my_action'}
        )

        COLLECT_PROFILE_DATA = '/usr/local/bin/collect-profile-data'
        exists.assert_any_call(COLLECT_PROFILE_DATA)
        check_output.assert_any_call([COLLECT_PROFILE_DATA])

    @mock.patch('charmbenchmark.action_set')
    def test_benchmark_finish(self, action_set):
        action_set.return_value = True
        self.assertTrue(Benchmark.finish())

    @mock.patch('charmbenchmark.Benchmark.set_data')
    def test_benchmark_set_composite_score(self, set_data):
        set_data.return_value = True
        self.assertTrue(Benchmark.set_composite_score(
            15.7, 'hits/sec', 'desc'))

    @mock.patch('charmbenchmark.Benchmark.set_data')
    @mock.patch('charmbenchmark.Benchmark.set_meta')
    def test_benchmark_meta(self, set_meta, set_data):
        key = 'foo'
        value = 'bar'
        units = 'bogomips'
        direction = 'desc'

        # Test with only a key/value pair
        Benchmark.set_meta(key, value)
        set_meta.assert_called_once_with(key, value)

        # set_data.side_effect = [True]
        # set_data.assert_has_calls([
        #     mock.call({'meta.%s' % key: value})
        #     #set_data({'meta.asdf': value})
        # ])
        # Benchmark.set_data({'meta.%s.value' % key: value})
        # Benchmark.set_data({'meta.%s.units' % key: units})
        # Benchmark.set_data({'meta.%s.direction' % key: direction})
        # set_data.reset_mock()
        set_meta.reset_mock()

        # Test with all parameters
        Benchmark.set_meta(key, value, units, direction)
        set_meta.assert_called_once_with(key, value, units, direction)
        pass
