from pathlib import Path
from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = tuple(f.readlines())

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('scripts.ini', 'r', encoding='utf-8') as f:
    entry_points = f.read()

package_dir = 'turmyx'

with (Path(package_dir) / '_version.py').open() as f:
    _vars = dict()
    exec(f.read(), _vars)
    version = _vars.get('__version__', '0.0.0')
    del _vars

setup(
    name='turmyx',
    version=version,
    packages=find_packages(exclude=('tests.*', 'tests')),

    url='',
    author='Ismael Benito',
    author_email='',
    description='',
    long_description=long_description,

    install_requires=requirements,
    entry_points=entry_points,
)
