from setuptools import setup, find_packages

setup(
    name='climateservaccess',
    version='0.0.1',
    author='Adam Zheng',
    author_email='adzheng@tamu.edu',
    description='A custom library for accessing the ClimateSERV API',
    long_description=open('README.md').read(),
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