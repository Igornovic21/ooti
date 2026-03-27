# Décisions d'architecture

Ce document explique les choix structurels effectués dans ce projet, ainsi que les compromis que chacun implique.

---

## 1. Sens des dépendances : qui connaît qui ?

La question centrale est : quelle application importe des données de l'autre ?

```
todos ──── FK ───▶ notes
```

`Todo` possède une `ForeignKey` pointant vers `Note`. Cela signifie :

- `todos` dépend de `notes` (au niveau du modèle, via une référence de chaîne `'notes.Note'`)

- `notes` ne connaît rien de `todos` — elle n'importe jamais de données de `todos`

Ceci donne un graphe de dépendances clair et unidirectionnel. L'application `notes` est un module autonome ; `todos` est le consommateur. Vous pourriez extraire `notes` dans son propre service demain sans modifier son code.

**Pourquoi ne pas utiliser un champ ManyToManyField sur `Note` ?**

Une relation ManyToManyField sur `Note` ferait de `notes` le propriétaire de la relation, l'obligeant à importer `Todo`. Cela inverserait la dépendance : l'application de bas niveau connaîtrait l'application de haut niveau. Mauvaise direction.

---

## 2. Comment `notes` expose ses tâches associées sans importer `todos`

`NoteSerializer` utilise `SerializerMethodField` et l'accesseur inverse de l'ORM (`obj.todo_set`) ; aucune importation de `Todo` ou `TodoSerializer` n'est nécessaire au chargement du module.

```python
def get_todos(self, obj):

return list(obj.todo_set.values('id', 'title', 'status'))
```

Lorsque `NoteViewSet` a besoin de l'intégralité de `TodoSerializer` (pour la sous-action `/todos`), il l'importe **dans le corps de la fonction** :

```python
@action(detail=True, methods=['get'], url_path='todos')
def todos(self, request, pk=None):

from todos.serializers import TodoSerializer # importation différée

...
```

Ceci évite toute importation circulaire lors de l'initialisation du module tout en permettant la sérialisation inter-applications lorsque nécessaire. C'est un compromis délibéré : un léger défaut de conception (importation tardive) en échange d'une structure de modules propre.

---

## 3. Modèle à deux champs sur TodoSerializer : `note` + `note_detail`

```python

note = PrimaryKeyRelatedField(...) # modifiable, accepte un ID (ou null)

note_detail = NoteMinimalSerializer(source='note', read_only=True) # intégration en lecture seule
```

**Pourquoi deux champs ?**

- Les écritures doivent être simples : `{"note": 1}` ou `{"note": null}`. Pas de création d'objet imbriqué.

- Les lectures doivent être utiles : renvoyer uniquement `"note": 1` force un second appel API. L'intégration de `note_detail` évite cet aller-retour.

Il s'agit d'un modèle DRF courant. L'alternative — un sérialiseur imbriqué unique et modifiable — ajoute de la complexité (il faudrait une fonction `update()` personnalisée pour décider de créer ou de lier la note) sans aucun avantage ici.

---

## 4. `on_delete=SET_NULL` sur la clé étrangère

```python
note = models.ForeignKey('notes.Note', null=True, blank=True, on_delete=models.SET_NULL)

```

Si une note est supprimée, ses tâches ne sont **pas** supprimées ; elles perdent simplement la référence. C'est le comportement correct : une tâche continue d'exister même si la note à laquelle elle est liée est supprimée.

`CASCADE` supprimerait silencieusement les tâches, ce qui est dangereux. `PROTECT` empêcherait la suppression des notes, ce qui est trop restrictif.

---

## 5. `select_related` / `prefetch_related` au niveau du ViewSet

```python
# TodoViewSet
queryset = Todo.objects.select_related('note')

# NoteViewSet
queryset = Note.objects.prefetch_related('todo_set')
```

Sans ces fonctions, l'affichage de 100 tâches déclencherait 101 requêtes (N+1). Ces deux lignes corrigent ce problème au niveau du ViewSet, ce qui est transparent pour les sérialiseurs et ne nécessite aucune solution de contournement pour chaque vue.

---

## 6. Absence de barre oblique finale dans `DefaultRouter`

```python
router = DefaultRouter(trailing_slash=False)
```

Les utilisateurs de Postman et cURL oublient souvent la barre oblique finale. La redirection 301 par défaut de Django en cas de barre oblique manquante peut convertir silencieusement une requête POST en GET, entraînant la perte du corps de la requête. Désactiver la vérification de la barre oblique finale élimine ce problème.

---

## 7. `NoteMinimalSerializer` — un modèle de lecture dédié

Plutôt que de réutiliser l'intégralité de `NoteSerializer` dans `TodoSerializer` (ce qui imbriquerait des listes de tâches, créant une boucle récursive), un `NoteMinimalSerializer` dédié expose uniquement `id` et `title`.

Il s'agit de l'équivalent, pour un sérialiseur, d'un DTO/projection : exposer exactement ce dont le consommateur a besoin, rien de plus.

---

## 8. Fonctionnalités omises (et raisons)

| Fonctionnalité | Décision |

|---------|----------|

| Authentification | Omise — l'exercice demande des points de terminaison fonctionnels ; l'authentification ajoute de la surface d'exposition sans démontrer l'architecture |

| Pagination | Ignorée — facile à ajouter via `DEFAULT_PAGINATION_CLASS` dans les paramètres |

| Filtrage / Recherche | Ignoré — `django-filter` s'intègre parfaitement, mais ce n'est pas l'objectif ici |

| Tests | Ignoré par manque de temps — utilisation de `APITestCase` + fixtures |

| `django.contrib.admin` | Supprimé — pas d'authentification, pas d'administration, pour minimiser `INSTALLED_APPS` |

| Base de données de production | SQLite — suffisante pour une revue locale |

---

## Démarrer le projet en local

---

## Résumé de la structure de l'application

```
ooti/ # Paramètres du projet, URL racine

notes/ # Application autonome — aucune connaissance des tâches

models.py # Modèle de note

serializers.py # NoteSerializer (avec données de tâches différées), NoteMinimalSerializer

views.py # NoteViewSet + sous-action /todos (importation différée)

urls.py # Route