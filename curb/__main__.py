import click
import psutil
import subprocess
import os
import signal
import sys
from time import sleep
import json


class ConditionSet:
    def __init__(self, ram, cpu, verbose):
        self.ram, self.cpu, self.verbose = self._cast(ram, cpu, verbose)

    def _cast(self, ram, cpu, verbose):
        """FIXME: Add error messages & handing for incorrect params"""
        ram, cpu, verbose = (
            float(ram[:-2]),
            float(cpu[:-1]),
            (verbose == "True"),
        )

        if verbose:
            print(
                "ConditionSet initialized with RAM={}MB & CPU={}%".format(
                    ram, cpu
                )
            )

        return ram, cpu, verbose

    def conditional_terminate(self, cpu, ram, sigterm):
        if cpu <= self.cpu and ram <= self.ram:
            if self.verbose:
                print(
                    "Process continuing with RAM: {}MB & CPU: {}%".format(
                        ram, cpu
                    )
                )
            return

        breaker = "CPU" if cpu > self.cpu else "RAM"
        limit = self.cpu if breaker == "CPU" else self.ram
        value = cpu if breaker == "CPU" else ram
        print(
            "Resource {} exceeded limit of {} with value of {}".format(
                breaker, limit, value
            )
        )
        sigterm()


class LatencyInterval:
    def __init__(self, latency):
        self.latency = self._cast(latency)

    def _cast(self, latency):
        """FIXME: Add error messages & handing for incorrect params"""
        return int(latency[:-1])

    def wait(self):
        sleep(self.latency)


def process_config(config_path):
    def _read_json(path):
        with open(path, "r") as f:
            return json.load(f)

    if config_path is None:
        return None, None

    config = None

    try:
        config = _read_json(config_path)
    except Exception as e:
        print(
            "Config file-read error encountered with exception {}\nIgnoring config file for now.".format(
                e
            )
        )
        config = None

    if config is None:
        return None, None

    cpu, ram = None, None

    if "cpu" in config:
        cpu = config["cpu"]

    if "ram" in config:
        ram = config["ram"]

    return cpu, ram


def sigterm(pid, parent_exit=True):
    p = psutil.Process(pid)
    p.terminate()
    print("SIGTERM: Killing curb module")

    if parent_exit:
        exit()


@click.command()
@click.option(
    "--cmd", help="The command that you'd want to curb (ex: 'node app.js')"
)
@click.option(
    "--cpu",
    default="100%",
    help="CPU limit in % (default: '100%') of a single core - decimals work too!",
)
@click.option(
    "--ram",
    default="512mb",
    help="RAM limit in megabytes (default: '512mb') - decimals work too, but I'm not sure why you would do that to yourself.",
)
@click.option(
    "--config",
    default=None,
    help='Path to a JSON config file that may/may not contain entries with the "ram" or "cpu" keys. If it does, then these values override the defaults/CLI args passed in.',
)
@click.option(
    "--verbose",
    default="False",
    help="Verbose setting, may be 'False' or 'True'",
)
@click.option(
    "--latency",
    default="1s",
    help="The time-interval at which the passed command is monitored, in seconds (default: '1s'",
)
def run(cmd, cpu, ram, config, verbose, latency):
    li = LatencyInterval(latency)
    pro = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
    pid = pro.pid
    _cpu, _ram = process_config(config)
    ram = _ram if _ram is not None else ram
    cpu = _cpu if _cpu is not None else cpu
    cs = ConditionSet(ram, cpu, verbose)

    def _get_datapoints(process):
        cpu = process.cpu_percent()
        ram_bytes = process.memory_info().rss
        ram = ram_bytes * 1.0 / (1024 * 1024)

        if cs.verbose:
            print(
                "Current Process CPU: {}% & RAM: {} bytes ({} MB)".format(
                    cpu, ram_bytes, ram
                )
            )

        return cpu, ram

    if cs.verbose:
        print(
            "Setting signal.SIGINT to map to our internal sigterm() function call"
        )

    signal.signal(signal.SIGINT, lambda s, f: sigterm(pid))
    try:
        while True:
            p = psutil.Process(pid)
            cpu, mem = _get_datapoints(p)
            cs.conditional_terminate(cpu, mem, lambda: sigterm(pid))
            li.wait()
    except Exception as e:
        sigterm(pid, parent_exit=False)
        print(
            "Exception encountered across event loop. Details:\n{}".format(e)
        )


run()