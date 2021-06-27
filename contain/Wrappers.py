from time import sleep


class ConditionSet:
    def __init__(self, ram, cpu, verbose):
        self.ram, self.cpu, self.verbose = self._cast(ram, cpu, verbose)

    def _cast(ram, cpu, verbose):
        """FIXME: Add error messages & handing for incorrect params"""
        return float(ram[:-2]), float(cpu[:-3]), (verbose == "True")

    def conditional_terminate(self, cpu, ram, sigterm):
        if cpu <= self.cpu and ram <= self.ram:
            if self.verbose:
                print(
                    "Process continuing with CPU: {} & RAM: {}".format(
                        cpu, ram
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

    def _cast(latency):
        """FIXME: Add error messages & handing for incorrect params"""
        return int(latency[:-1])

    def wait(self):
        sleep(self.latency)
