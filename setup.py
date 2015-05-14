from setuptools import setup

install_requires = [
    'PyYAML',
    'charmhelpers'
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
            'benchmark-start=charmbenchmark.cli.start:main',
            'benchmark-finish=charmbenchmark.cli.finish:main',
            'benchmark-actions=charmbenchmark.cli.actions:main',
            'benchmark-composite=charmbenchmark.cli.composite:main',
        ]
    }
)
