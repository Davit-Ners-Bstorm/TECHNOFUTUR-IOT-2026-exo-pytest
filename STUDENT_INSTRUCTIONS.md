# Parcours élève

Travaillez dans l'ordre. Commencez par un seul exemple clair, puis faites évoluer vos tests au fil des notions découvertes. Les noms de statuts se trouvent dans `iot/models.py`.

## Exercice 1 — Premier test

Créez `tests/test_temperature.py`. Écrivez un test simple qui vérifie le statut d'une température normale. Lancez ce fichier seul, puis rendez volontairement l'assertion fausse pour lire le message de PyTest.

## Exercice 2 — Frontières de température

Testez au minimum :

- une valeur normale ;
- la frontière basse de `WARNING` ;
- la frontière basse de `CRITICAL` ;
- les minimum et maximum autorisés ;
- deux valeurs juste hors de la plage valide.

Utilisez `pytest.raises` pour les valeurs invalides.

## Exercice 3 — Paramétrage

Refactorez les cas répétés de température avec `pytest.mark.parametrize`. Un cas doit correspondre à une ligne de données lisible. Ajoutez les valeurs immédiatement avant chaque changement de statut.

## Exercice 4 — Autres règles métier

Créez les fichiers de tests pour l'humidité, la qualité de l'air et la batterie. Pour chaque domaine, couvrez : minimum, maximum, chaque transition de statut, deux valeurs impossibles. Puis cherchez un cas non numérique ou non fini utile.

## Exercice 5 — Exceptions d'appareil

Construisez un faux capteur avec `Mock`. Vérifiez qu'une lecture normale retourne sa valeur et que `read()` est appelé exactement une fois. Testez ensuite :

- un appareil hors ligne ;
- une batterie à zéro ;
- une erreur provenant du matériel via `side_effect`.

Dans les deux premiers cas, vérifiez surtout que le capteur n'est jamais appelé.

## Exercice 6 — Fixtures et `conftest.py`

Transformez le capteur, l'appareil normal et le notifier en fixtures. Placez les fixtures réutilisées par plusieurs fichiers dans `tests/conftest.py`. Les fichiers de tests ne doivent pas importer ce module.

## Exercice 7 — Alertes

Testez séparément la décision d'alerte et la construction du message. Avec un notifier mocké, vérifiez :

- le message exact pour une mesure critique ;
- l'absence d'appel pour une situation normale ;
- un seul appel quand mesure et batterie sont critiques ensemble.

## Exercice 8 — Contrôleur

Testez l'enregistrement, la recherche, la suppression et le refus d'un identifiant dupliqué. Contrôlez ensuite le rapport d'une lecture normale.

Ajoutez deux appareils de types différents et vérifiez leurs classifications. Faites tomber l'un d'eux hors ligne : le rapport de l'autre doit toujours être présent.

## Exercice 9 — Pannes dans une collecte

À l'aide de `side_effect`, simulez une panne du capteur. Vérifiez le code d'erreur et son détail dans le rapport. Simulez également une mesure hors plage, puis distinguez les deux erreurs.

## Exercice 10 — TP final

Composez une flotte avec trois appareils : un normal, un critique et un défaillant. Vérifiez en une seule collecte :

- les trois entrées du rapport ;
- les statuts ou erreurs attendus ;
- le nombre et le contenu des notifications ;
- que chaque capteur pertinent a été appelé, ou non appelé.

Enfin, utilisez les marqueurs pour séparer tests unitaires et tests d'intégration. Essayez `-k`, `-m`, un chemin de fichier et un node id précis.

## Défis facultatifs

- Faites varier tous les appareils avec un paramétrage indirect de fixture.
- Ajoutez une notion d'historique sans casser l'API existante.
- Ajoutez un capteur de bruit et ses propres frontières.
- Rendez les messages d'erreur encore plus précis et testez-les.
- Identifiez les tests redondants et améliorez leur lisibilité.
