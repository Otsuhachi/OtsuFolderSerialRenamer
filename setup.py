import sys

from setuptools import find_packages, setup

with open('LICENSE', 'r', encoding='utf-8') as f:
    lcs = f.read()
info = sys.version_info
setup(
    name='otsufolserren',
    version='2022.8.12',
    description='[Windows Only!]フォルダ内のパスに対して連番リネームを行うライブラリです。',
    author='Otsuhachi',
    author_email='agequodagis.tufuiegoeris@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    license=lcs,
    install_requires=[
        'otsutil',
        'otsuvalidator',
    ],
)
