# Processus d'installation de modules Python pour QGIS sous Windows

Notes :

* L'installation d'un module Python tiers pour QGIS ne semble pas nécessiter que QGIS soit arrêter. Néanmoins il semble plus raisonnable qu'il soit arrêter avant de faire ces manipulations.
* Des modules Python installés avec des droits d'administrateur ne peuvent pas par la suite être modifiés (désinstallés ou mis à jour) sans ces droits d'administrateur. Si vous avez tendance à installer des modules tiers avec des droits d'administrateur, essayez de le faire de manière systématique.

## Installation pas à pas d'un module Python pour QGIS

1. Lancer PowerShell en mode admin
2. Se déplacer dans le répertoire de QGIS :

```bat
cd C:\Program Files\QGIS 3.28.10
```

3. Lancer OSGeo4W :

```bat
.\OSGeo4W.bat
```

4. Exécuter l'installation d'un module Python :

```bat
pip install pandas
```

## Même chose en appelant un script .bat

1. Créer un script pip-install.bat avec les instructions d'installation des modules Python

```bat
python -m pip install pandas
python -m pip install SQLAlchemy
```

2. Combiner les deux dernières étapes du processus précédent en une seule commande :

```bat
.\OSGeo4W.bat C:\path\to\pip-install.bat
```

## Utiliser un fichier requirements.txt

1. Créer un fichier requirements.txt

```txt
pandas
SQLAlchemy
```

2. Remplacer le contenu du fichier pip-install.bat :

```bat
python -m pip install -r C:\path\to\requirements.txt
```

3. Exécuter le script via OSGeo4W :

```bat
.\OSGeo4W.bat C:\path\to\pip-install.bat
```

## Mentionner les versions des modules dans le fichier requirements.txt

1. Ajouter les contraintes sur les numéros de version dans le fichier requirements.txt :

```txt
SQLAlchemy>=2.0.21, <3.0
pandas>=2.1.1, <3.0
```

2. Exécuter le script via OSGeo4W :

```bat
.\OSGeo4W.bat C:\path\to\pip-install.bat
```

## Script Python

Exemple de script Python pour exécuter l'installation des modules Python tiers dans QGIS en se basant sur le processus décrit précédemment :

```python
import subprocess
import os

last_cwd = os.getcwd()

QGIS_DIR = r"C:\Program Files\QGIS 3.28.10"
os.chdir(QGIS_DIR)

subprocess.run(
    [
        r"OSGeo4W.bat",
        r"C:\path\to\pip-install.bat",
    ]
)

os.chdir(last_cwd)

```

## Création d'un exécutable pour simplifier cette tâche

Le module pyinstaller permet de créer un exécutable pour le système d'exploitation sur lequel il est utilisé.
Ainsi en utilisant pyinstaller sous Windows on peut transformer un script Python en exécutable pour Windows.

Voir [Construire l'exécutable](./dev_build.md)
