import click
import psutil
import subprocess
import os
import signal

from Wrappers import ConditionSet, LatencyInterval


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
    default="1ghz",
    help="CPU limit in ghz (default: '1ghz') - decimals work too!",
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

    try:
        while True:
            p = psutil.Process(pid)
            stats = p.as_dict()
            cpu, mem = stats["cpu_percent"], stats["memory_percent"]
            cs.conditional_terminate(cpu, mem, lambda: sigterm(pid))
            li.wait()
    except Exception as e:
        sigterm(pid, parent_exit=False)
        print(
            "Exception encountered across event loop. Details:\n{}".format(e)
        )


if __name__ == "__main__":
    run()
