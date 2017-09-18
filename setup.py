from setuptools import setup

setup(
    name='strongr',
    version='1.0',
    description='An elastic cloud command runner',
    author='Thomas Phil',
    author_email='thomas@tphil.nl',
    packages=find_packages(),  #same as name
    install_requires=[], #external packages as dependencies
    scripts=[]
)
