<div align="center">

<img src="https://raghavmecheri.me/curb.png" width="600px">


**Resource containerization, quick and dirty**

---

<p align="center">
  <a href="#about-curb">About</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#implementation">Implementation</a> •
  <a href="#development">Development</a> •
  <a href="#meta">License</a>
</p>

[![PyPi Badge](https://img.shields.io/pypi/dm/curb?style=for-the-badge)](https://pypi.org/project/curb/)
[![PyPi Version](https://img.shields.io/pypi/v/curb?style=for-the-badge)](https://pypi.org/project/curb/)
[![Github Actions Build Status](https://img.shields.io/github/workflow/status/raghavmecheri/curb/Test?style=for-the-badge)](https://img.shields.io/github/workflow/status/raghavmecheri/curb/Test?style=for-the-badge)

</div>

---

## About Curb
Curb lets you resource-constrain processes rapidly for local development. Whether you're trying to mimic a remote machine's hardware constraints or just trying to make sure that a child process doesn't go crazy, Curb's got you covered.

## Installation
```sh
pip install curb
```

## Usage
Call curb from the command line with a child process call as a parameter to launch a tracked child process and monitor it with a given latency

### Samples
Launch a child process with the default hardware limitations that curb imposes (512 MB & 100% of a single CPU core):
```sh
python -m curb --cmd="python scripts/empty.py"
```

Launch a child process with custom hardware limitations and a defined latency (default=1s)
```sh
python -m curb --cmd="python scripts/empty.py" --cpu="80%" --ram="400mb" --latency="5s"
```

Launch a sample call based on a JSON hardware definition
`ssh
python -m curb --cmd="python scripts/empty.py" --config=".curbconfig.json" --latency="5s"
`

### Expected Config Structure
A `.curbconfig.json` file (an easy way to store your curb configuration) is expected to be of the format
```json
{
	"ram": "512MB",
	"cpu": "90%"
}
```

### Notes
The units of measure in both the config file and the config arguements to the command line are case-insensitive, but expected as a part of the input for those parameters. Megabytes are currently the only unit supported for `ram`.

## Implementation
Curb is implemented via the Python `subprocess` module, and utilizes the `psutil` library to pull system information. This tool is primarily meant to constrain resources in a development environment, and is not meant to be used as a container-based solution in any sort of latency-sensitive application.

## Development
### Install Dependancies
```sh
make install
```
### Run Sample
```sh
make sample
```
### Run Unit Tests
```sh
make test
```

## Meta
Distributed under the MIT license. See ``LICENSE`` for more information.
