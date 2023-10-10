# Gestionnaire FT - Extension pour QGIS

Utilitaire pour installer des modules tiers dans la distribution Python accompagnant QGIS.
Ne fonctionne que sous Windows.

Modules actuellement installés (voir ) :

* SQLAlchemy
* pandas
* openpyxl

----

## Usage

* on lance l'application (.exe pour Windows)
* après un court message d'explication l'application demande à l'utilisateur s'il souhaite continuer (répondre oui, non, yes, no, voire simplement o, y ou n)
* l'application recherche les versions de QGIS installées sur l'ordinateur
* s'il en trouve une seule il demande à l'utilisateur s'il souhaite installer les bibliothèques dedans
* s'il en trouve plusieurs il demande à l'utilisateur de choisir dans quel QGIS les bibliothèques doivent être installées
* l'application exécute alors le processus d'installation des bibliothèques (qui affichera un tas d'informations utiles en cas de problème)
* à la fin elle demande à l'utilisateur de taper sur la touche entrée pour fermer l'application 

----

## Licence

[GPL v3](LICENSE)

----

## Attribution

* Benjamin Chartier
* Utilisation du registre Windows pour détecter les versions de QGIS installées inspiré de Pablo Satler (see <https://gist.github.com/psatler/010b26cd57e758278823d7027c40e2a6>)
