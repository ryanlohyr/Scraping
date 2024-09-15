.PHONY: execute

execute:
	@python3 -m venv venv
	@source venv/bin/activate && pip install -r requirements.txt
	@npm install playwright
	@source venv/bin/activate && python3 main.py