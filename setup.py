import os

from setuptools import setup, find_packages

install_requires = [
    'PyYAML',
    'charmhelpers'
]

tests_require = [
    'coverage',
    'nose',
    'pep8',
]

HERE = os.path.dirname(__file__)
with open(os.path.join(HERE, 'VERSION')) as f:
    VERSION = f.read().strip()

setup(
    name='charm-benchmark',
    version=VERSION,
    description='Library to aid in the creation of benchmark actions in Juju',
    install_requires=install_requires,
    url="https://github.com/juju-solutions/charm-benchmark",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'benchmark-start = charmbenchmark.cli.start:main',
            'benchmark-finish = charmbenchmark.cli.finish:main',
            'benchmark-actions = charmbenchmark.cli.actions:main',
            'benchmark-composite = charmbenchmark.cli.composite:main',
            # An alias for benchmark-composite
            'benchmark-result = charmbenchmark.cli.composite:main',
            'benchmark-meta = charmbenchmark.cli.meta:main',
            'benchmark-data = charmbenchmark.cli.data:main',
            'benchmark-raw = charmbenchmark.cli.raw:main',
        ]
    }
)
