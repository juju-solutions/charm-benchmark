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

    From inside the benchmark-relation-changed hook, you would
    Benchmark(['memory', 'cpu', 'disk', 'smoke', 'custom'])

    Examples:

        siege = Benchmark(['siege'])
        siege.start()
        [... run siege ...]
        # The higher the score, the better the benchmark
        siege.set_composite_score(16.70, 'trans/sec', 'desc')
        siege.finish()


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
    def set_composite_score(value, units, direction='asc'):
        """
        Set the composite score for a benchmark run. This is a single number
        representative of the benchmark results. This could be the most
        important metric, or an amalgamation of metric scores.
        """
        try:
            action_set({
                "meta.composite": {
                    'value': value, 'units': units, 'direction': direction
                }
            })
            return True
        except OSError:  # File not found -- we're not in an action context
            return False

    @staticmethod
    def start():
        try:
            action_set({
                'meta.start': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            })

            """
            If the cabs-collector charm is installed, take a snapshot
            of the current profile data.
            """
            if os.path.exists(COLLECT_PROFILE_DATA):
                subprocess.check_output([COLLECT_PROFILE_DATA])
            return True
        except OSError:  # File not found -- we're not in an action context
            return False

    @staticmethod
    def finish():
        try:
            action_set({
                'meta.stop': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            })
            return True
        except OSError:  # File not found -- we're not in an action context
            return False
