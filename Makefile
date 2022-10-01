include .env
db = db-plan
app = plan

build:
	docker-compose up --build

destroy:
	docker system prune -a -f --volumes $(c)

db_connect:
	docker exec -it ${db} psql --username=${DB_USER} --dbname=${DB_NAME}

app_connect:
	docker exec -it ${app} sh
