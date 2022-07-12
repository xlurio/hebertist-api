# utils
run_command_on = docker-compose -f docker-compose.dev.yml run --rm
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
crawl_steam = "(crawl) steam_price

make_migrations = $(manage) makemigrations core && \
									$(manage) migrate

migrate = $(manage) migrate

test_backend = $(manage) test && flake8
test_crawler = python -m unittest

build:
	docker-compose build

crawl-games:
	${run_command_on} ${crawler} "${crawl_games}"; \
	docker-compose down

crawl-prices:
	$(run_command_on) ${crawler} "${crawl_prices}"

crawl-gog:
	${run_command_on} ${crawler} "${crawl_gog}"; \
	docker-compose down

crawl-steam:
	${run_command_on} ${crawler} "${crawl_steam}"; \
	docker-compose down

dismiss:
	docker-compose down

make-migrations:
	$(run_command_on) $(backend) "$(make_migrations)"

migrate:
	$(run_command_on) $(backend) "$(migrate)"

run:
	docker-compose up

test-all:
	$(run_command_on) $(backend) "$(test_backend)"; \
	$(run_command_on) $(crawler) "$(test_crawler)"; \
	docker-compose down

test-backend:
	$(run_command_on) $(backend) "$(test_backend)"

test-crawler:
	$(run_command_on) $(crawler) "$(test_crawler)"