server-down:
	@docker compose -f docker-compose-prod.yml down -v

server-up:
	@docker compose -f docker-compose-prod.yml up

sync:
	@cd /home/rodesousa/git/echo/echo/directus && ./sync.sh -u http://localhost:8055 push

worker-network:
	@docker exec -it devcontainer_backend_1 dramatiq-gevent --queues network --processes 3 --threads 50 dembrane.tasks

worker-cpu:
	@docker exec -it devcontainer_backend_1 dramatiq-gevent --queues cpu --processes 3 --threads 50 dembrane.tasks

restart-backend:
	@docker compose -f docker-compose-prod.yml restart backend

