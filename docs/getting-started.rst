Getting Started
===============

Benchmarks are `Juju Actions <https://jujucharms.com/docs/stable/actions>`_ that follow a specific pattern. While they can be accomplished via ``action_set``, we've created charm-benchmark to make that task easier.

Installing Charm Benchmark
--------------------------

    pip install charm-benchmark


Using charm-benchmark
---------------------

There are two ways of using charm-benchmark: via direct calls to the Python library...:

::

    #!/usr/bin/env python
    import subprocess

    try:
        from charmhelpers.core.hookenv import action_get
    except ImportError:
        subprocess.check_call(['apt-get', 'install', '-y', 'python-pip'])
        subprocess.check_call(['pip', 'install', 'charmhelpers'])
        from charmhelpers.contrib.benchmark import Benchmark

    try:
        from charmbenchmark import Benchmark
    except ImportError:
        import subprocess
        from charmhelpers.fetch import apt_install

        apt_install('python-pip', fatal=True)
        cmd = ['pip', 'install', '-U', 'charm-benchmark']
        subprocess.call(cmd)
        from charmbenchmark import Benchmark


    def main():

        Benchmark.start()

        # Get your parameters via action_get and run your benchmark

        # Parse the benchmark results
        transactions = 1096
        transaction_rate = 10.51
        transferred = 346.08
        response_time = 0.92

        Benchmark.set_data({'results.transactions.value': transactions})
        Benchmark.set_data({'results.transactions.units': 'hits'})

        Benchmark.set_data({'results.transaction_rate.value': transactions})
        Benchmark.set_data({'results.transaction_rate.units': 'hits/sec'})

        Benchmark.set_data({'results.transferred.value': transferred})
        Benchmark.set_data({'results.transferred.units': 'MB'})

        Benchmark.set_data({'results.response_time.value': response_time})
        Benchmark.set_data({'results.response_time.units': 'secs'})

        # Set the composite, which is the single most important score
        Benchmark.set_composite_score(
            transaction_rate,
            'hits/sec',
            'desc'
        )

        Benchmark.finish()


    if __name__ == "__main__":
        main()

...or via cli commands, which can be called from bash or any other language:

::

    #!/bin/bash
    set -eux
    benchmark-start || true

    # Run your benchmark

    # Grep/awk/parse the results

    benchmark-data 'transactions' 1096 'hits'
    benchmark-data 'transaction_rate' 10.51 'hits/sec'
    benchmark-data 'transferred' 346.08 'MB'
    benchmark-data 'response_time' 0.92 'ms'

    # Set the composite, which is the single most important score
    benchmark-composite 'transaction_rate' 10.51 'hits/sec' 'desc'

    benchmark-finish || true
