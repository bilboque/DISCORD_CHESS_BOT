# ChessApi
## Tool chain
On utilise les libraries interactions.py pour le bot discord et l'api de lichess pour les echecs:
- https://interactions-py.github.io/interactions.py/Guides/01%20Getting%20Started/          (a lire en priorité)
- https://interactions-py.github.io/interactions.py/API%20Reference/API%20Reference/Client/ (api ref discord)
- https://lichess.org/api   (api lichessapi lichess) // pas très interressant il faut ce réferrer a la doc de berserk si-dessous
- https://python-chess.readthedocs.io/en/latest/core.html   (python chess module) // pour la logique du jeu d'echec (obternir les coup légaux etc)
- https://lichess-org.github.io/berserk/usage.html  (lichess python client) // pour interagire avec la l'api lichess

## A LIRE SVP
On a 2 token pour lichess et un pour discord. Les files sont ".token" pour discord, ".tokenandres" et ".tokenleo" il ne faut pas les commits sur gitlab (en particulier pour .token et .tokenandres).
Il faut faire attention a utiliser des methodes asyncrones pour toute les fonctions du bot (en gros quand on envois un msg sur discord on met un await devant les methodes de interaction.py)
Pour les commandes tournois et resultats il faut que le bot tourne sur mon pc (leo) car les endpoints et la db du site tourne sur mon pc en local.

## TODO
- un file requirement.py probablement

