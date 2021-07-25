import pytest
import os
import json
from curb.Config import process_config

CONFIGS = [
    {"path": "./scripts/.curbconfig.json", "expected": (None, "512MB")},
    {"path": "./scripts/mock_bad_config.json", "expected": (None, None)},
    {"path": "randompathdoesnotexist", "expected": (None, None)},
]


@pytest.mark.parametrize("params", CONFIGS)
def test_config_processing(params):
    path, expected = params["path"], params["expected"]
    cpu, ram = process_config(path, True)
    e_cpu, e_ram = expected
    assert cpu == e_cpu
    assert ram == e_ram
