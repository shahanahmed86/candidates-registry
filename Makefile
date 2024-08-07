HOST=localhost
V1_PORT=28017

# development
run-dev-up:
	docker compose \
	-f docker-compose.yml -f docker-compose.dev.yml \
	up -d
run-dev-rebuild:
	docker compose \
	-f docker-compose.yml -f docker-compose.dev.yml \
	up -d --build --renew-anon-volumes
run-dev-down:
	docker compose \
	-f docker-compose.yml -f docker-compose.dev.yml \
	down
run-dev-down-hard:
	docker compose \
	-f docker-compose.yml -f docker-compose.dev.yml \
	down -v

run-migrate-create:
	REDIS_HOST="${HOST}" DB_HOST="${HOST}" DB_HOST_V1="${HOST}" DB_PORT_V1="${V1_PORT}" \
	npm run migrate create ${NAME}
run-migrate-up:
	REDIS_HOST="${HOST}" DB_HOST="${HOST}" DB_HOST_V1="${HOST}" DB_PORT_V1="${V1_PORT}" \
	npm run migrate up
run-migrate-down:
	REDIS_HOST="${HOST}" DB_HOST="${HOST}" DB_HOST_V1="${HOST}" DB_PORT_V1="${V1_PORT}" \
	npm run migrate down ${NAME}
run-migrate-prune:
	REDIS_HOST="${HOST}" DB_HOST="${HOST}" DB_HOST_V1="${HOST}" DB_PORT_V1="${V1_PORT}" \
	npm run migrate prune

# production
run-prod-up:
	docker compose \
	-f docker-compose.yml -f docker-compose.prod.yml \
	up -d
run-prod-down:
	docker compose \
	-f docker-compose.yml -f docker-compose.prod.yml \
	down
