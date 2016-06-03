from os import path
from setuptools import setup, find_packages
import codecs


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = codecs.decode(f.read(), 'utf-8') 

setup(
    name='winmoncon',
    version='0.0.0',
    description='A Python inteface to the Windows Monitor Configuration API',
    long_description=long_description,
    author='Mihai Ciumeică',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    packages=find_packages(exclude=['tests', 'docs', 'examples'])
)
