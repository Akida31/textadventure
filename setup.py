try:
    from setuptools import setup, find_packages
except ModuleNotFoundError:
    from distutils.core import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='Python Roleplay-Game',
    version='0.0.1a',
    author='Akida',
    description='An own created game to test the abilities of Python',
    licens='MIT',
    keywords='game commandline',
    long_description=long_description,
    packages=find_packages()

)
