compile:
	docker-compose run --rm web bash ./compile.sh

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

run:
	docker-compose up
