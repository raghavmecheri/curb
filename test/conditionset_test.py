import pytest
import os
import json

from curb.utils import ConditionSet, LatencyInterval, process_config

CASES = [
    {"lim_cpu": "100%", "lim_ram": "1mb", "cpu": 300.0, "ram": 0},
    {"lim_cpu": "100%", "lim_ram": "1mb", "cpu": 0.0, "ram": 3.0},
    {"lim_cpu": "100%", "lim_ram": "1mb", "cpu": 300.0, "ram": 3.0},
    {"lim_cpu": "100%", "lim_ram": "3mb", "cpu": 30.0, "ram": 0.0},
]

CONFIGS = [
    {"path": "./scripts/mock_config.json", "expected": (None, "512MB")},
    {"path": "./scripts/mock_bad_config.json", "expected": (None, None)},
    {"path": "randompathdoesnotexist", "expected": (None, None)},
]


class MethodCallLogger(object):
    def __init__(self, meth):
        self.meth = meth
        self.call_count = 0

    def __call__(self, *args):
        self.meth(*args)
        self.call_count += 1


def _compute_expected_count(lim_cpu, lim_ram, cpu, ram):
    if cpu > lim_cpu:
        return 1
    elif ram > lim_ram:
        return 1
    return 0


@pytest.mark.parametrize("params", CONFIGS)
def test_config_processing(params):
    path, expected = params["path"], params["expected"]
    cpu, ram = process_config(path)
    e_cpu, e_ram = expected
    assert cpu == e_cpu
    assert ram == e_ram


@pytest.mark.parametrize("params", CASES)
def test_condition_set(params):
    lim_cpu, lim_ram, cpu, ram = (
        params["lim_cpu"],
        params["lim_ram"],
        params["cpu"],
        params["ram"],
    )
    cs = ConditionSet(lim_ram, lim_cpu, False)
    f = MethodCallLogger(lambda: None)
    cs.conditional_terminate(cpu, ram, f)
    assert f.call_count == _compute_expected_count(cs.cpu, cs.ram, cpu, ram)
