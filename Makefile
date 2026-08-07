.PHONY: env update format lint test

# Créer l'environnement localement
env:
	conda env create -p ./.conda -f environment.yml
	conda run -p ./.conda pre-commit install

# Mettre à jour l'environnement local
update:
	conda env update -p ./.conda -f environment.yml --prune

# Lancer les outils via l'environnement local
format:
	conda run -p ./.conda ruff format src/ tests/
	conda run -p ./.conda ruff check --fix src/ tests/

lint:
	conda run -p ./.conda ruff check src/ tests/
	conda run -p ./.conda mypy src/

train:
	conda run -p ./.conda python src/mon_projet_ml/train.py

test:
	conda run -p ./.conda pytest tests/
