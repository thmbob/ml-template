# ACCEL : variante matérielle de PyTorch (gpu | cpu).
# Détectée automatiquement, surchargeable : make env ACCEL=cpu
ACCEL ?= $(shell command -v nvidia-smi >/dev/null 2>&1 && echo gpu || echo cpu)

# Préfixe d'exécution. La CI le vide (CONDA_RUN=) car l'environnement
# y est déjà activé dans le shell.
CONDA_RUN ?= conda run --no-capture-output -p ./.conda

.PHONY: help env update lock format lint test train clean

.DEFAULT_GOAL := help

help:  ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

env:  ## Crée l'environnement local (.conda) et installe les hooks git
	conda env create -p ./.conda -f environment.$(ACCEL).yml
	conda env update -p ./.conda -f environment.yml
	$(CONDA_RUN) pip install -e .
	$(CONDA_RUN) pre-commit install

update:  ## Met à jour l'environnement local
	conda env update -p ./.conda -f environment.$(ACCEL).yml
	conda env update -p ./.conda -f environment.yml --prune
	$(CONDA_RUN) pip install -e .

lock:  ## Fige les versions exactes dans conda-lock.yml
	$(CONDA_RUN) conda-lock lock -f environment.yml -f environment.$(ACCEL).yml \
		-p linux-64 -p osx-arm64 -p win-64

format:  ## Formate et corrige automatiquement le code
	$(CONDA_RUN) ruff format src/ tests/
	$(CONDA_RUN) ruff check --fix src/ tests/

lint:  ## Vérifie le style et les types (sans rien modifier)
	$(CONDA_RUN) ruff format --check src/ tests/
	$(CONDA_RUN) ruff check src/ tests/
	$(CONDA_RUN) mypy src/

test:  ## Lance la suite de tests
	$(CONDA_RUN) pytest tests/

train:  ## Vérifie l'installation en entraînant un modèle jouet
	$(CONDA_RUN) python src/mon_projet_ml/train.py

clean:  ## Supprime les caches d'outils
	rm -rf .pytest_cache .ruff_cache .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
