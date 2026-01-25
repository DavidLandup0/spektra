lint:
	uv run ruff check .

format:
	uv run ruff format .

style: lint format

headers:
	python3 header/create_header.py
