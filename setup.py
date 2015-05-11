from setuptools import setup

install_requires = [
    'PyYAML',
]

tests_require = [
    'coverage',
    'nose',
    'pep8',
]


setup(
    name='charm-benchmark',
    version='0.0.1',
    description='Library to aid in the creation of benchmark actions in Juju',
    install_requires=install_requires,
    url="https://launchpad.net/~cabs-team",
    packages=['charmbenchmark'],
    entry_points={
        'console_scripts': [
            'benchmark-start=charmbenchmark.Benchmark:start',
            'benchmark-finish=charmbenchmark.Benchmark:finish',
        ]
    }
)
