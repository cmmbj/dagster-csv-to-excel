# 🚀 Projet : Convertisseur Batch CSV vers Excel avec Dagster

Ce projet est un pipeline de données automatisé construit avec **Dagster**. Il permet de convertir **en masse** tous les fichiers `.csv` présents dans un dossier d'entrée vers des fichiers `.xlsx` (Excel), tout en conservant leur nom d'origine.


## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir installé :
* **Python** (version 3.8 ou supérieure)
* **Pip** (gestionnaire de paquets Python)

---

## ⚙️ Installation

1.  Ouvrez votre terminal à la racine du projet (là où se trouve le fichier `pyproject.toml`).
2.  Installez le projet et ses dépendances en mode éditable :

```bash
pip install -e .

```

> **Note :** Cette commande installe automatiquement `dagster`, `dagster-webserver`, `pandas` et `openpyxl`.

---

## 🏃 Utilisation

### 1. Préparer les données

Déposez vos fichiers `.csv` bruts dans le dossier suivant :
`csv_to_excel_project/data/inputs/`

### 2. Lancer le serveur Dagster

Dans votre terminal (à la racine du projet), lancez la commande :

```bash
dagster dev

```

### 3. Exécuter la conversion

1. Ouvrez votre navigateur et allez sur : [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000)
2. Dans le menu de gauche, cliquez sur l'asset **`convert_all_csvs`**.
3. Cliquez sur le bouton bleu **"Materialize"** (en haut à droite).

### 4. Récupérer les résultats

Une fois l'exécution terminée (asset devenu vert), vos fichiers Excel convertis se trouvent ici :
`csv_to_excel_project/data/outputs/`

---

## 📂 Structure du Projet

Voici comment est organisé le projet :

```text
DAGSTER-CSV-TO-EXCEL/
├── pyproject.toml              # Configuration et liste des dépendances
├── README.md                   # Documentation (Vous êtes ici)
└── csv_to_excel_project/       # Code source du projet
    ├── __init__.py             # Définitions Dagster (Câblage)
    ├── assets.py               # Logique de conversion (Code Python)
    └── data/
        ├── inputs/             # 📥 Mettre vos CSV ici
        └── outputs/            # 📤 Récupérer vos Excel ici

```

---

## 🛠️ Dépannage & Astuces

* **J'ai modifié le code, mais rien ne change dans l'interface ?**
Cliquez sur le bouton **"Reload Definitions"** dans l'interface web (souvent en haut à droite) pour recharger le code sans redémarrer le serveur.
* **Erreur "File not found" ?**
Vérifiez que vos dossiers `data/inputs` et `data/outputs` existent bien à l'intérieur du dossier `csv_to_excel_project`.
* **Le serveur tourne toujours ?**
Pour arrêter le serveur Dagster dans le terminal, faites `CTRL + C`.

```

```