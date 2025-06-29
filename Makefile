.PHONY: up
up:
	docker compose up -d --build

.PHONY: down
down:
	docker compose down

.PHONY: stop
stop:
	docker compose stop

.PHONY: build
build:
	docker compose build

.PHONY: logs
logs:
	docker compose logs -f
