# ⚠️ Remplacer `latest` par un tag daté pour rendre l'image reproductible.
# Les tags disponibles : https://hub.docker.com/r/condaforge/miniforge3/tags
FROM condaforge/miniforge3:latest

# Variante PyTorch : gpu (défaut) ou cpu
ARG ACCEL=gpu

# Utilisateur non-root : évite que les fichiers créés dans le conteneur
# ressortent en root sur le volume monté côté hôte.
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID --create-home $USERNAME \
    && chown -R $USER_UID:$USER_GID /workspace

# 1. Environnement : couche lourde, ne dépend que des fichiers environment.*
#    Elle reste en cache tant que les dépendances ne changent pas.
COPY environment.yml environment.${ACCEL}.yml ./
RUN conda env create -p /opt/conda/env -f environment.${ACCEL}.yml && \
    conda env update -p /opt/conda/env -f environment.yml && \
    conda clean -afy

ENV PATH="/opt/conda/env/bin:$PATH"

# 2. Code : couche légère, invalidée à chaque modification.
#    Séparée de l'étape 1 pour ne pas relancer un solve conda à chaque commit.
COPY pyproject.toml ./
COPY src/ ./src/
RUN pip install -e . --no-deps

USER $USERNAME

SHELL ["/bin/bash", "-c"]
CMD ["/bin/bash"]
