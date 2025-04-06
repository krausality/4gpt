from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='4gpt',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,  # Ensure package data (like config.json) is included
    package_data={
        'forgpt': ['config.json'],  # Specify that config.json is included in the twogpt package
    },
    install_requires=[
        'dir-tree @ git+https://github.com/krausality/dir_tree.git',
    ],
    entry_points={
        'console_scripts': [
            '4gpt=forgpt.core:main',  # Adds `4gpt` command to the CLI
        ],
    },
    author='krausality',
    author_email='github@krausality.com',
    description='A CLI tool for generating an `allfiles.txt` report of a directory, with inclusion and exclusion rules managed through a `.gptignore` file and a centralized config.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/krausality/4gpt',  # Update this if hosting the package
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.9',
)
