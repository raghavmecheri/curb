install:
	python -m pip install -r requirements.txt

sample:
	python contain/main.py --cmd="python scripts/empty.py" --verbose="True"
