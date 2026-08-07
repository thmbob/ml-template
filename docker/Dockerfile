FROM condaforge/miniforge3:latest

# Définition du répertoire de travail dans le conteneur
WORKDIR /workspace

# Installation des outils système essentiels (git, build-essential pour certains paquets C++)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie du fichier d'environnement
COPY environment.yml pyproject.toml ./
COPY src/ ./src/

# Création de l'environnement Conda dans un chemin fixe (/opt/conda/env)

RUN conda env create -p /opt/conda/env -f environment.yml && conda clean -afy

# Ajout de l'environnement dans le PATH par défaut du conteneur
ENV PATH="/opt/conda/env/bin:$PATH"

# Shell par défaut
SHELL ["/bin/bash", "-c"]
CMD ["/bin/bash"]
