"""setup file for BetterLoader deployments
"""

from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="contain",
    version="0.0.1",
    description="A minimalist module to containerize child processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raghavmecheri/contain",
    author="Raghav Mecheri",
    author_email="raghav@binit.in",
    license="MIT",
    download_url="https://github.com/raghavmecheri/contain",
    packages=["contain"],
    install_requires=["click==8.0.1", "psutil==5.8.0"],
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
