install:
	python -m pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

test: FORCE
	python -m pytest

build:
	TESTBUILD="True" python -m build

test-release:
	TESTBUILD="True" twine upload --repository testpypi dist/*

sample:
	python -m curb --cmd="python scripts/empty.py" --verbose="True"

heavy-sample:
	python -m curb --cmd="python scripts/consumer.py" --cpu="100%" --ram="256mb" --verbose="True"

config-sample:
	python -m curb --cmd="python scripts/empty.py" --config=".curbconfig.json" --verbose="True"

FORCE: