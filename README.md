# Recherche de sous-pages Google Sites

Ce dépôt contient un petit outil Python pour tester une liste de sous-pages possibles
sur un site Google Sites (ex: `https://sites.google.be/indse/be/geographie/...`).

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests
```

## Utilisation

```bash
python search_subpages.py \
  --base "https://sites.google.be/indse/be/geographie" \
  --words wordlist.txt \
  --workers 8 \
  --timeout 10
```

### Sauver les résultats

```bash
python search_subpages.py \
  --base "https://sites.google.be/indse/be/geographie" \
  --words wordlist.txt \
  --output found.txt
```

## Personnaliser la liste de mots

Éditez `wordlist.txt` et ajoutez les noms de pages que vous souhaitez tester.
Les lignes vides et celles commençant par `#` sont ignorées.
