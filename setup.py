from setuptools import setup

setup(
    name='commandr',
    version='1.0',
    description='A python commandbus implementation',
    author='Thomas Phil',
    author_email='thomas@tphil.nl',
    packages=['commndr'],  #same as name
    install_requires=['bar', 'greek'], #external packages as dependencies
    scripts=[]
)
