# Makefile :^)

main_image = convergent

docker_build_args = \
	--build-arg GIT_COMMIT=$(shell git show -s --format=%H) \
	--build-arg GIT_COMMIT_DATE="$(shell git show -s --format=%ci)" \
	--build-arg IMAGE_NAME=$(service) \
	--build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%T.%N%Z") \
	--build-arg VER_PYTHON=$(python_version) \
	--build-arg VER_PIP=$(pip_version) \
	

black: 
	black utility/
	black tests/
	black convergent/

requirements.txt:
	pip-compile --generate-hashes --quiet -B requirements.in

build:
	DOCKER_BUILDKIT=1 docker-compose build convergent --no-cache
	
run: 
	docker-compose -p convergent up convergent

setup-local-db:
	docker-compose -p update-local-db build update-local-db && \
	docker-compose -p update-local-db up update-local-db

test:
	docker-compose -p convergent-ci run -e TAG=latest --rm ci

prune:
	docker system prune --volumes --all

purge:
	docker builder prune -a \
 		&& docker-compose down --volumes \
  		&& docker-compose down --rmi all -v \
  		&& docker-compose build --no-cache \
 		&& docker-compose  -f docker-compose.yml up -d --force-recreate

clean:
	docker rmi -f $(main_image)
