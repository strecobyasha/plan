include .env
db = db-plan
app = plan

help:
	@echo "Makefile commands:"
	@echo "build"
	@echo "destroy"
	@echo "db_connect"
	@echo "app_connect"
build:
	docker-compose up --build
destroy:
	docker system prune -a -f --volumes $(c)
db_connect:
	docker exec -it ${db} psql --username=${DB_USER} --dbname=${DB_NAME}
app_connect:
	docker exec -it ${app} sh
