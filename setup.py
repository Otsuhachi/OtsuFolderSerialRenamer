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
    classifiers=[
        'Development Status :: 1 - Planning',
        'Natural Language :: Japanese',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'License :: OSI Approved :: MIT License',
    ],
    license=lcs,
    keywords='Python Python3 フォルダ ディレクトリ serial_number serial_rename rename 連番 連番リネーム 変更 監視 monitoring',
    install_requires=[
        'otsutil',
        'otsuvalidator',
    ],
)
