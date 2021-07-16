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
