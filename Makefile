# utils
run_command_on = docker-compose run --rm
on_shell = sh -c

# services
backend = api $(on_shell)
crawler = crawler $(on_shell)

# commands
test_backend = "python manage.py test && flake8"
test_crawler = "python -m unittest"

run:
	docker-compose up

dismiss:
	docker-compose down

test-all:
	$(run_command_on) $(backend) $(test_backend); \
	$(run_command_on) $(crawler) $(test_crawler); \
	docker-compose down

test-backend:
	$(run_command_on) $(backend) $(test_backend); \
	docker-compose down

test-crawler:
	$(run_command_on) $(crawler) $(test_crawler); \
	docker-compose down