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
