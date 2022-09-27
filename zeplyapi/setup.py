import os
import sys
from setuptools import setup, find_packages


__dir__ = os.path.abspath(os.path.dirname(__file__))

BIN_DIR = os.path.dirname(sys.executable)
PACKAGE_NAME = "zeplyapi"


def get_version():
    version_info = {}
    version_file_path = os.path.join(
        __dir__, 'src', PACKAGE_NAME, 'versioninfo.py')
    with open(version_file_path) as f:
        exec(f.read(), version_info)
    return version_info['VERSION']


def get_requirements():
    requirements = []
    with open(os.path.join(__dir__, 'requirements.txt')) as f:
        for line in f:
            req = line.strip()
            if not req:
                continue
            requirements.append(req)
    return requirements


def read_package_file(path):
    with open(os.path.join(__dir__, path), 'r') as f:
        return f.read()


setup(
    name=PACKAGE_NAME,
    version=get_version(),
    license='Apache GNU License 2.0',
    author="Andrea Di Franco",
    author_email="difranco.developer@gmail.com",
    description = ("zeplyapi project for creating and retrieving blockchain addresses"),
    long_description=read_package_file('README.md'),
    zip_safe=True,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires=">=3.7",
    install_requires=get_requirements(),
    data_files=[
        ('', ['requirements.txt']),
    ],
)
