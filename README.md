# ml-template

Squelette de projet Machine Learning : PyTorch, environnement conda reproductible,
outillage qualité (ruff, mypy, pytest, pre-commit), conteneur et devcontainer prêts.

## Démarrage

```bash
git clone <url-du-projet> && cd <projet>
make env          # crée ./.conda, installe le package et les hooks git
make train        # entraîne un modèle jouet : valide l'installation de bout en bout
```

`make env` détecte la présence d'un GPU NVIDIA (via `nvidia-smi`) et choisit la
variante PyTorch correspondante. Pour forcer :

```bash
make env ACCEL=cpu
```

## Commandes

`make` seul affiche la liste. Les principales :

| Commande       | Effet                                                     |
| -------------- | --------------------------------------------------------- |
| `make env`     | Crée l'environnement local et installe les hooks git       |
| `make update`  | Réaligne l'environnement sur les fichiers `environment.*`  |
| `make format`  | Formate et corrige automatiquement                         |
| `make lint`    | Vérifie style et types, sans rien modifier                 |
| `make test`    | Lance la suite de tests                                    |
| `make lock`    | Fige les versions exactes dans `conda-lock.yml`            |
| `make clean`   | Supprime les caches d'outils                               |

Le `Makefile` est la seule interface : le jour où l'environnement change de
gestionnaire, les commandes ci-dessus ne bougent pas.

## Structure

```
src/mon_projet_ml/     Code source (package installé en editable)
tests/                 Tests pytest
notebooks/             Exploration — les sorties sont nettoyées au commit
docker/                Image de référence
.devcontainer/         Environnement VS Code conteneurisé
data/                  Données — ignoré par git, sauf data/sample/
experiments/           Sorties d'entraînement — ignoré par git
```

## Environnement

Trois fichiers, parce que seule la pile PyTorch dépend du matériel :

- `environment.yml` — base commune à toutes les plateformes
- `environment.gpu.yml` — PyTorch variante CUDA
- `environment.cpu.yml` — PyTorch variante CPU (macOS, machines sans GPU, CI)

Les versions sont bornées (`>=` version testée, `<` prochaine majeure).
Pour une reproduction stricte, `make lock` produit un `conda-lock.yml`
avec les versions et les hashes exacts.

**Attention** : `ruff` est épinglé dans `environment.yml` *et* dans
`.pre-commit-config.yaml`. Les deux doivent rester alignés, sinon `make format`
et le hook git se contredisent. Un `pre-commit autoupdate` implique de reporter
la nouvelle version dans `environment.yml`.

## Docker

```bash
docker build -f docker/Dockerfile -t mon-projet-ml .
docker run --rm -it --gpus all -v "$PWD":/workspace mon-projet-ml
```

VS Code : « Reopen in Container » utilise la même image via `.devcontainer/`.

## Adapter le template à un nouveau projet

Le nom `mon_projet_ml` apparaît dans `pyproject.toml`, le `Makefile`, les tests
et le chemin `src/`. À renommer d'un coup :

```bash
NEW=mon_nouveau_projet
git mv src/mon_projet_ml "src/$NEW"
grep -rl mon_projet_ml --exclude-dir=.git . | xargs sed -i "s/mon_projet_ml/$NEW/g"
```

## Qualité

`pre-commit` tourne à chaque commit : formatage, tri des imports, nettoyage des
sorties de notebooks, refus des fichiers volumineux. La CI GitHub Actions rejoue
ces hooks, puis `mypy` et `pytest` sur un environnement CPU reconstruit à neuf.

Pour tout passer manuellement :

```bash
pre-commit run --all-files
```
