# API F1

## Descrition

Cette API fournit des données complètes et détaillées sur la Formule 1, incluant les saisons, circuits, pilotes, écuries, résultats de courses, qualifications, arrêts au stand, et bien plus encore.
Elle s’appuie sur une base de données MongoDB et expose des endpoints REST pour faciliter l’accès et l’analyse des données historiques et statistiques de la Formule 1.

## Installation

### Etape 1 :
Créer une base de donées **MongoDB** et la nommer `f1` *(ou autre mais pensez à bien renseigner le noms plus tard)*.

### Etape 2 :
Créer un fichier `.env` à la racine du projet et y ajouter les variables d'environnement suivantes :

```env
MONGO_URI=mongodb://host:port
DB_NAME=f1 # Ou votre nom de la base de données

DATA_PATH=./data
```
### Etape 3 :
Installer les dépendances du projet :

```bash
pip install -r requirements.txt
```

### Etape 4 :
Lancer le script d'import des données :

```bash
python import_data.py
```

### Etape 5 :
Lancer le serveur FastAPI :

```bash
flask run
```

## Utilisation

### Accéder à l'API
L'API est accessible par défaut à l'adresse suivante : `http://localhost:8000`.

### Documentation de l'API

[Cliquez ici](./ROUTES.md)  pour accéder à la documentation de l'API.
