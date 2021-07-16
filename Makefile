install:
	python -m pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

test: FORCE
	python -m pytest

sample:
	python contain --cmd="python scripts/empty.py" --verbose="True"

heavy-sample:
	python contain --cmd="python scripts/consumer.py" --cpu="100%" --ram="256mb" --verbose="True"

FORCE: