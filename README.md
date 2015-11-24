[![Build Status](https://travis-ci.org/juju-solutions/charm-benchmark.svg?branch=master)](https://travis-ci.org/juju-solutions/charm-benchmark)
[![Build Status](http://drone.dasroot.net/api/badge/github.com/juju-solutions/charm-benchmark/status.svg?branch=master)](http://drone.dasroot.net/github.com/juju-solutions/charm-benchmark)
[![Coverage Status](https://coveralls.io/repos/juju-solutions/charm-benchmark/badge.svg)](https://coveralls.io/r/juju-solutions/charm-benchmark)

# Deprecation notice:

This project has been deprecated and replaced by [http://github.com/juju-solutions/charms.benchmark](charms.benchmark). Please use that library instead. This one is no longer maintained.

# charm-benchmark

charm-benchmark provides commands to ease the development of benchmark charms. You can either import the python library into your action, or use the equivalent CLI commands.

    #!/bin/bash

    benchmark-start || true

    ... (your code goes here) ...

    benchmark-finish || true

# Installation

    $ pip install charm-benchmark

# Development

    $ python setup.py develop
