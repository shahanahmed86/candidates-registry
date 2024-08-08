run-container-up:
	docker compose up -d
run-container-rebuild:
	docker compose up -d --build --renew-anon-volumes
run-container-down:
	docker compose down
run-container-down-hard:
	docker compose down -v
