run:
	cp -n .env.example .env || true
	docker-compose up
install:
	poetry install
test:
	cp -n .env.example .env || true
	poetry run pytest tests