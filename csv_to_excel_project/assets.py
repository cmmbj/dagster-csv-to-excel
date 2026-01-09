# Importation du module 'os' pour gérer les chemins de dossiers (Windows/Mac/Linux)
import os

# Importation de Pandas, l'outil standard pour manipuler des données, renommé en 'pd'
import pandas as pd

# Importation des outils nécessaires depuis la librairie Dagster
# 'asset' est le décorateur, 'AssetExecutionContext' permet d'envoyer des logs (messages)
from dagster import asset, AssetExecutionContext

# Le décorateur @asset transforme la fonction python ci-dessous en un composant Dagster
@asset
def htsdata_excel(context: AssetExecutionContext):
    """
    Cet asset lit le fichier CSV htsdata et le convertit en fichier Excel.
    """
    
    # --- ÉTAPE 1 : DÉFINIR LES CHEMINS (PATHS) ---
    
    # On récupère le chemin absolu du dossier où se trouve CE fichier (assets.py)
    # Cela permet d'éviter les erreurs "Fichier non trouvé"
    current_dir = os.path.dirname(__file__)

    # On construit le chemin complet vers le fichier CSV d'entrée
    # Cela correspond à : .../csv_to_excel_project/data/inputs/htsdata (41 to 70).csv
    input_path = os.path.join(current_dir, "data", "inputs", "htsdata (41 to 70).csv")

    # On construit le chemin complet vers le futur fichier Excel de sortie
    output_path = os.path.join(current_dir, "data", "outputs", "htsdata_converti.xlsx")

    # --- ÉTAPE 2 : CHARGEMENT DES DONNÉES ---

    # On envoie un message dans l'interface de Dagster pour dire qu'on commence
    context.log.info(f"Lecture du fichier CSV depuis : {input_path}")

    # On utilise Pandas pour lire le fichier CSV et le mettre en mémoire (dans une variable 'df')
    # 'df' signifie DataFrame (c'est comme un tableau Excel virtuel)
    df = pd.read_csv(input_path)

    # --- ÉTAPE 3 : SAUVEGARDE EN EXCEL ---

    # On envoie un message pour dire qu'on a réussi à lire et qu'on écrit le fichier
    context.log.info(f"Écriture du fichier Excel vers : {output_path}")

    # On demande à Pandas de prendre ce tableau 'df' et de l'écrire en fichier Excel
    # index=False signifie qu'on ne veut pas ajouter une colonne de numérotation (0, 1, 2...)
    df.to_excel(output_path, index=False)

    # On retourne le chemin final pour que Dagster puisse l'afficher ou l'utiliser plus tard
    return output_path