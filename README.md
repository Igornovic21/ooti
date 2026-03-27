# Backend (Django + DRF)

API REST construite avec Django et Django REST Framework pour la gestion de **todos** et **notes**.

---

## Stack technique

* Python 3.x
* Django
* Django REST Framework
* SQLite (par défaut)

---

## Installation en local

### 1. Cloner le projet

```bash
git clone https://github.com/Igornovic21/ooti.git
cd ooti
```

---

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

### Activer l’environnement

#### 🐧 Linux / macOS

```bash
source venv/bin/activate
```

#### 🪟 Windows

```bash
venv\Scripts\activate
```

---

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

### 4. Configurer les variables d’environnement

Créer un fichier `.env` à la racine (optionnel si déjà configuré) :

```env
DEBUG=True
SECRET_KEY=your-secret-key
```

---

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

---

### 6. Créer un super utilisateur (optionnel)

```bash
python manage.py createsuperuser
```

---

### 7. Lancer le serveur

```bash
python manage.py runserver
```

👉 API disponible sur :
http://127.0.0.1:8000/

---

## 📡 Endpoints principaux

### Todos

```bash
GET     /api/todos/
POST    /api/todos/
GET     /api/todos/{id}/
PUT     /api/todos/{id}/
DELETE  /api/todos/{id}/
```

---

### Notes

```bash
GET     /api/notes/
POST    /api/notes/
GET     /api/notes/{id}/
PUT     /api/notes/{id}/
DELETE  /api/notes/{id}/
```

---

## 📂 Structure du projet

```bash
project/
├── ooti/
├── todos/
├── notes/
└── manage.py
```

---

## 👨‍💻 Auteur

Projet réalisé dans le cadre d’un exercice technique backend Django.
