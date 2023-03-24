.PHONY: install
install: ## install requirements
	pip install -r requirements.txt

.PHONY: run-backend
run-backend: ## Run backend
	python manage.py runserver