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


class TestBenchmarkCli(TestCase):

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
        
