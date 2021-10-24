"""setup file for curb deployments
"""
__version__ = "0.0.5"
__test_version__ = "0.0.5"

from setuptools import setup, find_packages
from io import open
from os import path, getenv

import pathlib

version = __test_version__ if getenv("TESTBUILD") == "True" else __version__
base_url, package_name = "https://github.com/raghavmecheri/curb", "curb"

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=package_name,
    version=version,
    description="A minimalist module to containerize child processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),  # list of all packages
    install_requires=["click==8.0.1", "psutil==5.8.0"],
    python_requires=">=3.6",
    entry_points="""
        [console_scripts]
        curb=curb.__main__:main
        """,
    author="Raghav Mecheri",
    author_email="raghav@binit.in",
    license="MIT",
    download_url="{0}/archive/{1}-{2}".format(base_url, package_name, version),
    keyword="curb, container, resource",
    url="https://github.com/raghavmecheri/{}".format(package_name),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.8",
    ],
)
