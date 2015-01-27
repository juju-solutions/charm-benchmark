#!/usr/bin/env python
import time
from .common import action_set


def main():
    action_set('meta.start', time.strftime('%Y-%m-%dT%H:%M:%SZ'))

if __name__ == "__main__":
    main()
