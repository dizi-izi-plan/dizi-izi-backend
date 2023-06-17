.PHONY: install
install: ## install requirements
	pip install -r requirements.txt

.PHONY: run-backend
run-backend: ## Run backend
	python manage.py runserver

WORKDIR = .
MANAGE = python $(WORKDIR)/manage.py

style:
	black -S -l 79 $(WORKDIR)
	isort $(WORKDIR)
	flake8 $(WORKDIR)
