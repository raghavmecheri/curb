from __future__ import absolute_import

import click
import psutil
import subprocess
import os
import signal
import sys

from .Wrappers import ConditionSet, LatencyInterval
from .Config import process_config


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
