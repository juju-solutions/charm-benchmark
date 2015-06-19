import subprocess
import os
import time
from charmhelpers.core.hookenv import (
    action_get,
    action_set,
    in_relation_hook,
    relation_get,
    relation_set,
    relation_ids
)

COLLECT_PROFILE_DATA = '/usr/local/bin/collect-profile-data'


class Benchmark():
    """
    Helper class for the `benchmark` interface.

    :param list actions: Define the actions that are also benchmarks


    Examples:

    Notify the Benchmark GUI of the actions that are benchmark-enabled, usually run from benchmark-relation-[joined|changed]::

        Benchmark(['memory', 'cpu', 'disk', 'smoke', 'custom'])


    From within a benchmark-enabled action::

        # Begins timing of a benchmark
        Benchmark.start()

        [... run benchmark and parse results ...]

        Benchmark.set_data({'results.transactions.value': 1096})
        Benchmark.set_data({'results.transactions.units': 'hits'})

        # Store a meta key, available via ``juju action fetch`` but not shown in the Benchmark GUI
        Benchmark.set_meta('myuuid', '1b231f32-16c3-11e5-ac89-14109fd63717')

        # The higher the score, the better the benchmark
        Benchmark.set_composite_score(16.70, 'hits/sec', 'desc')

        # Finish the timing of a benchmark
        Benchmark.finish()
    """

    required_keys = [
        'hostname',
        'port',
        'graphite_port',
        'graphite_endpoint',
        'api_port'
    ]

    def __init__(self, benchmarks=None):
        if in_relation_hook():
            if benchmarks is not None:
                for rid in sorted(relation_ids('benchmark')):
                    relation_set(relation_id=rid, relation_settings={
                        'benchmarks': ",".join(benchmarks)
                    })

            # Check the relation data
            config = {}
            for key in self.required_keys:
                val = relation_get(key)
                if val is not None:
                    config[key] = val
                else:
                    # We don't have all of the required keys
                    config = {}
                    break

            if len(config):
                with open('/etc/benchmark.conf', 'w') as f:
                    for key, val in iter(config.items()):
                        f.write("%s=%s\n" % (key, val))

    @staticmethod
    def set_data(value):
        """
        Set the key:value to be passed to ``action_set``

        :param list value: A hash containing the key and value
        """
        try:
            action_set(value)
            return True
        except OSError:
            return False

    @staticmethod
    def set_composite_score(value, units='', direction=None):
        """
        Set the composite score for a benchmark run. This is a single number
        representative of the benchmark results. This could be the most
        important metric, or an amalgamation of metric scores.
        """
        Benchmark.set_data({'meta.composite.value': value})

        # The GUI expects this key, even if it's empty
        Benchmark.set_data({'meta.composite.units': units})

        if direction:
            Benchmark.set_data({'meta.composite.direction': direction})
        return True

    @staticmethod
    def set_meta(key, value):
        Benchmark.set_data({'meta.%s.value' % key: value})

    @staticmethod
    def start():
        """
        If the cabs-collector charm is installed, take a snapshot
        of the current profile data.
        """
        if os.path.exists(COLLECT_PROFILE_DATA):
            subprocess.check_output([COLLECT_PROFILE_DATA])

        return Benchmark.set_data({
            'meta.start': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        })

    @staticmethod
    def finish():
        return Benchmark.set_data({
            'meta.stop': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        })
