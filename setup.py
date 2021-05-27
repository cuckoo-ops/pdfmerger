import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def get_requires(filename):
    requirements = []
    with open(filename, 'r') as req_file:
        for line in req_file.read().splitlines():
            line_stripped = line.strip()
            if line_stripped[:1] not in ('#', '-'):
                requirements.append(line_stripped)
    return requirements


def load_name_version():
    '''Loads a file content'''
    filename = os.path.abspath(os.path.join(here, 'pdf_merger', '__init__.py'))
    with open(filename, "rt") as name_version_file:
        content = name_version_file.read()
        version = re.search("__version__ = '([0-9a-z.-]+)'", content).group(1)
        app_name = re.search("__app_name__ = '(\S+)'", content).group(1)
        return app_name, version


with open("README.md", "r") as fh:
    long_description = fh.read()
pkg = find_packages(exclude=['test', ])
app_name, version = load_name_version()

setup(
    name=app_name,
    version=version,
    description='pcd',
    long_description=long_description,
    install_requires=get_requires(os.path.join(here, 'requirements.txt')),
    packages=pkg,
    tests_require=['pytest'],
    url='',
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
    include_package_data=True,
    entry_points={'console_scripts': ['pdfmerger=pdf_merger.main:main']
    }
)
