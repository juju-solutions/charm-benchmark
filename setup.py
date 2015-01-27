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
    name='benchmark_tools',
    version='0.0.1',
    description='Utilities to ease the development of benchmarks',
    install_requires=install_requires,
    url="https://launchpad.net/~cabs-team",
    packages=['benchmark_tools'],
    entry_points={
        'console_scripts': [
            'benchmark-start=benchmark_tools.start:main',
            'benchmark-finish=benchmark_tools.finish:main',
        ]
    }
)
