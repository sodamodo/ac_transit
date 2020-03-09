
#!/usr/bin/env bash
docker-compose -f docker-compose.yaml down
docker-compose -f docker-compose.yaml build
docker-compose -f docker-compose.yaml up --force-recreate
