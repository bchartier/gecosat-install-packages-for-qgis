# Construire l'exécutable

Ce programme est exclusivement destiné à fonctionner sous Windows.

Il doit être construit sous Windows pour Windows à l'aide de pyinstaller.

## Pré-requis : disposer d'un environnement Python et de pyinstaller

1. Créer un environnement Python virtuel :

```bat
python -m venv venv
```

2. Installer packages Python utilisés pour créer l'installeur :

```bat
pip install pyinstaller Jinja2 prompt_toolkit
```

## Créer l'exécutable

1. Activer l'environnement virtuel Python :

```bat
.\venv\Script\activate
```

2. Se placer à la racine du code source du projet : le répertoire qui contient les sous-répertoires ""src" et "docs".
3. Lancer pyinstaller

```bat
pyinstaller -F src\install_packages_for_qgis.py --add-data "src/config;config"
```

4. Désactiver l'environnement virtuel Python

```bat
deactivate
```

L'exécutable est créé dans le répertoire "dist".
