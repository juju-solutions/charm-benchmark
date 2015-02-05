#!/usr/bin/env python
import time
from .common import action_set
import subprocess
import os

COLLECT_PROFILE_DATA = '/usr/local/bin/collect-profile-data'


def main():
    action_set('meta.start', time.strftime('%Y-%m-%dT%H:%M:%SZ'))
    if os.path.exists(COLLECT_PROFILE_DATA):
        subprocess.check_output([COLLECT_PROFILE_DATA])

if __name__ == "__main__":
    main()
