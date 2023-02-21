# Context 
L'indicateur __Least Square Moving Average (LSMA)__ vous permet d'évaluer la direction du mouvement du marché et ses éventuels renversements. Il est basé sur le calcul d'une régression linéaire OLS sur chaque fenêtre glissante (ex. 25 jours). C'est une bonne altérnative au moyenne mobile (MA).

Dans ce projet, on va mettre en place une régression OLS sur le marché boursier pour estimer les valeurs de la moyenne mobile des moindres carrés et enfin nous mettons en place une stratégie de trading simple avec la `LSMA` et la testons sur un ensemble de cours.

La stratégie a été adaptée d'[Algovibes](https://www.youtube.com/watch?v=sESQpRoo994), une [chaîne](https://www.youtube.com/@Algovibes) dédiée aux algorithmes de Trading avec Python.

## Comment ça marche ?
- On execute une régression OLS sur certaines fenêtres (n) (ex. 25 jours)
- Les variables `indépendantes` : `X = jour1, jour2, jour3, ...`
- La variable à expliquer `y = Close Price` : le prix

L'idée c'est d'avoir une prédiction pour chaque jour, basée sur la régression dans les `n` derniers jours (ex. 25).

Nous allons donc lancer une centaine de régressions.

# Les données
Les données utilisées dans ce projet sont issue de [Yahoo Finance](https://fr.finance.yahoo.com/).
La liste des symboles disponible sur [Yahoo Finance](https://fr.finance.yahoo.com/) est téléchargeable sur Python avec ce code :

```
liste_symbo = pd.read_csv("https://raw.githubusercontent.com/shilewenuw/get_all_tickers/master/get_all_tickers/tickers.csv", header=None)
```
Un script Python (`y finance downloader`) pour télécharger les symboles est disponible sur [Github ici](https://github.com/Benny-/Yahoo-ticker-symbol-downloader).

# Installation des packages
`$ pip install -r requirements.txt`

# Stratégie de Trading
Acheter si `Close > LSMA` value et vendre si `Close < LSMA` value.

> :warning: **Avis de non-responsabilité :**: Toutes les informations contenues sur ce projet sont uniquement destinées à des fins éducatives et ne constituent pas un conseil en investissement ou une sollicitation pour acheter ou vendre un instrument financier. Le trading peut vous exposer à un risque de perte supérieur à vos dépôts et ne convient qu'aux investisseurs expérimentés qui disposent de moyens financiers suffisants pour supporter un tel risque.

# Execution du code

## Paramètres d'entrée :
* `crypto` : l'action 
* `LSMA_Period`s : la période de calcul de la moyenne mobile selon la méthode des moindres carrés (ex. à partir de 01/01/2020)
* `window` : la fenetre glissante (ex. 25 pour 25 jours).