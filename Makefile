# utils
docker_compose = docker-compose -f docker-compose.yml -f docker-compose.dev.yml
run_command_on = $(docker_compose) run --rm
on_shell = sh -c
manage = python manage.py
crawl = scrapy crawl

# services
backend = api $(on_shell)
crawler = crawler $(on_shell)

# commands
crawl_games = python game_crawler.py
crawl_prices = python price_crawler.py
crawl_gog = $(crawl) gog_price
crawl_steam = "$(crawl) steam_price
run_worker = python worker.py

make_migrations = $(manage) makemigrations core && \
									$(manage) migrate

migrate = $(manage) migrate

test_backend = $(manage) test && flake8
test_crawler = python -m unittest && flake8

build:
	$(docker_compose) build

crawl-games:
	${run_command_on} ${crawler} "${crawl_games}"; \
	$(docker_compose) down

crawl-prices:
	$(run_command_on) ${crawler} "${crawl_prices}"

crawl-gog:
	${run_command_on} ${crawler} "${crawl_gog}"; \
	$(docker_compose) down

crawl-steam:
	${run_command_on} ${crawler} "${crawl_steam}"; \
	$(docker_compose) down

dismiss:
	$(docker_compose) down

make-migrations:
	$(run_command_on) $(backend) "$(make_migrations)"

migrate:
	$(run_command_on) $(backend) "$(migrate)"

run:
	$(docker_compose) up

test-all:
	$(run_command_on) $(backend) "$(test_backend)"; \
	$(run_command_on) $(crawler) "$(test_crawler)"; \
	$(docker_compose) down

test-backend:
	$(run_command_on) $(backend) "$(test_backend)"

test-crawler:
	$(run_command_on) $(crawler) "$(test_crawler)"

run-worker:
	$(run_command_on) $(crawler) "$(run_worker)"