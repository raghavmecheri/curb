# Curb
[![PyPi Badge](https://img.shields.io/pypi/dm/curb?style=for-the-badge)](https://pypi.org/project/curb/)
[![PyPi Version](https://img.shields.io/pypi/v/curb?style=for-the-badge)](https://pypi.org/project/curb/)
[![Github Actions Build Status](https://img.shields.io/github/workflow/status/raghavmecheri/curb/Build?style=for-the-badge)](https://img.shields.io/github/workflow/status/raghavmecheri/curb/Build?style=for-the-badge)

A lightweight and simple hardware virtualisation CLI for resource consumption management.

## Use Cases:
1. I'm developing a web app and my staging/prod VM has limits set on CPU/RAM - I want to test my app out locally with the same limits to make sure nothing goes wrong
2. I want to run a process, and I don't want it to consume resources past a certain limit on my computer

## Usage:
### Sample Call
`python -m curb --cmd="python scripts/empty.py"`
### Sample Call With Limits
`python -m curb --cmd="python scripts/empty.py" --cpu="100%" --ram="512mb"`
### More Information
`python -m curb --help`
