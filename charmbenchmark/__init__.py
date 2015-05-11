import subprocess
import os
import time
from charmhelpers.core.hookenv import (
    action_get,
    action_set
)

COLLECT_PROFILE_DATA = '/usr/local/bin/collect-profile-data'


class Benchmark:

    @staticmethod
    def start():
        action_set({
            'meta.start': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        })
        if os.path.exists(COLLECT_PROFILE_DATA):
            subprocess.check_output([COLLECT_PROFILE_DATA])
        return True

    @staticmethod
    def finish():
        action_set({
            'meta.stop': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        })
        return True
