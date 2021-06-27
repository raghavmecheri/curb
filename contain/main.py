import click
import psutil
import subprocess
import os
import signal
import sys

from Wrappers import ConditionSet, LatencyInterval, convert_unit


def sigterm(pid, parent_exit=True):
    p = psutil.Process(pid)
    p.terminate()
    print("SIGTERM: Killing contain module")

    if parent_exit:
        exit()


@click.command()
@click.option(
    "--cmd", help="The command that you'd want to contain (ex: 'node app.js')"
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
    "--verbose",
    default="False",
    help="Verbose setting, may be 'False' or 'True'",
)
@click.option(
    "--latency",
    default="1s",
    help="The time-interval at which the passed command is monitored, in seconds (default: '1s'",
)
def run(cmd, cpu, ram, verbose, latency):
    li = LatencyInterval(latency)
    pro = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
    pid = pro.pid
    cs = ConditionSet(ram, cpu, verbose)

    def _get_datapoints(process):
        cpu = process.cpu_percent()
        ram = convert_unit(process.memory_info().rss, 3)
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


if __name__ == "__main__":
    run()
