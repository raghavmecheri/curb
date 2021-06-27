install:
	python -m pip install -r requirements.txt

sample:
	python contain/main.py --cmd="python scripts/empty.py"

heavy-sample:
	python contain/main.py --cmd="python scripts/consumer.py" --cpu="1ghz" --ram="256mb" --verbose="True"
