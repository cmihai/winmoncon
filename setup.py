from os import path
from setuptools import setup, find_packages
import codecs


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = codecs.decode(f.read(), 'utf-8') 

setup(
    name='winmoncon',
    version='0.0.1',
    description='A Python inteface to the Windows Monitor Configuration API',
    long_description=long_description,
    author='Mihai Ciumeică',
    license='Public Domain',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: Public Domain',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(exclude=['tests', 'docs', 'examples'])
)
