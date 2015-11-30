import os

from setuptools import setup, find_packages

install_requires = [
    'PyYAML',
    'charms.benchmark>=1.0.2,<1.1'
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
)
