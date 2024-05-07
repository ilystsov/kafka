run:
	cp -n .env.example .env || true
	docker-compose up
install:
	poetry install
test:
	poetry run pytest tests