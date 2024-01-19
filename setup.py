#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from codecs import open
from pathlib import Path
from operator import itemgetter
import re
from typing import Iterable, List, Union

from setuptools import setup, find_packages

dependencies = {
    'build': {
        'setuptools',
        'wheel',
    },
    'docs': {
        'sphinx',
        'sphinx_rtd_theme',
    },
    'jupyter': {
        'jupyter',
        'jupyterlab>=3',
        'kaleido',
        'protobuf<4',
    },
    'mongo': {
        'pymongo',
    },
    'profile': {
        'memory_profiler',
        'snakeviz',
    },
    'postgres': {
        'psycopg2-binary',
        'sqlalchemy',
    },
    'ray': {
        'gpustat==1.0.0',
        'optuna',
        'ray[default,air,serve,tune]',
    },
    'test': {
        'Faker',
        'git-lint',
        'pytest',
        'pytest-cov',
        'pytest-pycodestyle',
        'pytest-sugar',
    },
}


def combine_dependencies(extras: Union[str, Iterable[str]]) -> List[str]:
    """
    Combine package dependencies.

    :param extras: key(s) from the `dependencies` dictionary
    :return: The minimum set of package dependencies contained in `extras`.
    """
    if isinstance(extras, str):
        deps = set(itemgetter(extras)(dependencies))
    else:
        deps = set().union(*itemgetter(*extras)(dependencies))
    return list(deps)


with open('minim/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(),
                        re.MULTILINE).group(1)

here = Path(__file__).absolute().parent
with open(here / 'README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Budd-E',
    version=version,
    description='Budd-E is a LLM agnostic AI Bot',
    author='Minh Nguyen',
    author_email='mthnguyen@outlook.com',
    license='BSD',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Build Tools',
    ],
    keywords='LLM, Large Language Models, AI, Bot, GenAI, GenerativeAI, AI '
             'Assistant',
    packages=find_packages(exclude=[
        'applications*',
        'data',
        'docker',
        'docs',
        'notebooks',
        'wheels',
        '*tests',
    ]),
    install_requires=[
        'captum',
        'click',
        'dash',
        # 'dask',
        'lovely-tensors',
        # 'matplotlib',
        'mlflow',
        # 'pandas',
        'plotly',
        'pyyaml',
        # 'torch',
        # 'torchdata',
        'torchmetrics',
        # 'torchvision',
        'ujson',
        'yapf',
    ],
    extras_require={
        'all':
        combine_dependencies(dependencies.keys()),
        'build':
        combine_dependencies(('build', 'test')),
        'docs':
        combine_dependencies('docs'),
        'jupyter':
        combine_dependencies('jupyter'),
        'mongo':
        combine_dependencies([x for x in dependencies if 'postgres' not in x]),
        'postgres':
        combine_dependencies([x for x in dependencies if 'mongo' not in x]),
        'profile':
        combine_dependencies('profile'),
        'ray':
        combine_dependencies('ray'),
        'test':
        combine_dependencies('test'),
    },
    package_dir={'minim': 'minim'},
    include_package_data=True,
    entry_points={'console_scripts': [
        'count=minim.cli:count',
    ]})

if __name__ == '__main__':
    pass
