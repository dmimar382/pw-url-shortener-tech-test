COMPOSE_FILE_DIR=deploy

build:
	docker compose -f $(COMPOSE_FILE_DIR)/docker-compose.yaml build

up:
	docker compose -f $(COMPOSE_FILE_DIR)/docker-compose.yaml up --build -d

stop:
	docker compose -f $(COMPOSE_FILE_DIR)/docker-compose.yaml stop

down:
	docker compose -f $(COMPOSE_FILE_DIR)/docker-compose.yaml down

logs:
	docker compose -f $(COMPOSE_FILE_DIR)/docker-compose.yaml logs -f

restart:
	make down && make up

clean:
	docker system prune -f

shell:
	docker compose -f $(COMPOSE_FILE_DIR)/docker-compose.yaml exec $(service) /bin/sh
