## Problème

Dans Pix Admin, sur l'écran de recherche d'organisations, quand je saisis du texte (par exemple `foo`) dans le champ ID puis que je lance la recherche, l'interface affiche le message générique **« Erreur dans Ember »** et aucun résultat ne s'affiche.

## Reproduction

1. Se connecter à Pix Admin avec un compte Pix Master
2. Aller sur la liste des organisations
3. Dans le filtre par ID, saisir une valeur non numérique (ex. `foo`)
4. Lancer la recherche

→ L'appel à `GET /api/organizations?filter[id]=foo` part vers l'API et la réponse fait planter l'UI ("Erreur dans Ember").

## Comportement attendu

Saisir un ID non numérique est une simple erreur de frappe côté utilisateur ; ça ne devrait pas faire planter quoi que ce soit. La requête devrait être rejetée proprement par l'API au lieu d'aller jusqu'au bout du traitement.

Les autres cas de recherche doivent continuer à fonctionner normalement :
- aucun critère de recherche
- ID numérique existant
- recherche par nom
