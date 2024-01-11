from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='climateservaccess',
    version='1.0.0',
    author='Adam Zheng',
    author_email='adzheng@tamu.edu',
    description='A custom library for accessing the ClimateSERV API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/adamzhen/climateservAccess',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
