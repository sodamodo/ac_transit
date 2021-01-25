down:
	docker-compose -f docker-compose.yaml down
cd
up: down
	docker-compose -f docker-compose.yaml build
	docker-compose -f docker-compose.yaml up -d --force-recreate

