# Importation du module 'os' pour naviguer dans les dossiers et gérer les noms de fichiers
import os

# Importation de Pandas pour la manipulation des données
import pandas as pd

# Importation des outils Dagster
from dagster import asset, AssetExecutionContext

@asset
def convert_all_csvs(context: AssetExecutionContext):
    """
    Cet asset scanne le dossier 'inputs', trouve tous les fichiers CSV,
    et les convertit en Excel en gardant le même nom.
    """

    # --- ÉTAPE 1 : DÉFINITION DES DOSSIERS ---

    # Récupération du dossier où se trouve ce script (assets.py)
    current_dir = os.path.dirname(__file__)

    # Chemin du dossier d'entrée (où sont les CSV)
    inputs_folder = os.path.join(current_dir, "data", "inputs")

    # Chemin du dossier de sortie (où iront les Excel)
    outputs_folder = os.path.join(current_dir, "data", "outputs")

    # --- ÉTAPE 2 : LISTER LES FICHIERS À TRAITER ---

    # On demande à Python de nous donner la liste de tout ce qu'il y a dans 'data/inputs'
    all_files = os.listdir(inputs_folder)

    # On crée une liste vide pour stocker les chemins des fichiers traités (pour le rapport final)
    processed_files = []

    # --- ÉTAPE 3 : LA BOUCLE (TRAITEMENT PAR LOTS) ---
    
    # On commence une boucle : "Pour chaque fichier (filename) dans la liste (all_files)..."
    for filename in all_files:

        # CONDITION : On vérifie si le fichier finit bien par ".csv" (pour ignorer les autres fichiers)
        if filename.endswith(".csv"):
            
            # --- 3.1 PRÉPARATION DES NOMS ---

            # On construit le chemin complet du fichier source (ex: .../inputs/mon_fichier.csv)
            input_path = os.path.join(inputs_folder, filename)

            # ASTUCE : On sépare le nom du fichier de son extension pour récupérer juste le nom
            # ex: "mon_fichier.csv" devient ("mon_fichier", ".csv") -> on prend le premier élément [0]
            file_root_name = os.path.splitext(filename)[0]

            # On crée le nouveau nom avec l'extension .xlsx
            # ex: "mon_fichier" + ".xlsx" -> "mon_fichier.xlsx"
            new_filename = file_root_name + ".xlsx"

            # On construit le chemin complet de sortie
            output_path = os.path.join(outputs_folder, new_filename)

            # --- 3.2 CONVERSION ---

            # On loggue un message pour dire quel fichier on est en train de traiter
            context.log.info(f"🔄 Traitement de : {filename} -> {new_filename}")

            # Lecture du CSV
            df = pd.read_csv(input_path)

            # Écriture en Excel (garder le même nom de base)
            df.to_excel(output_path, index=False)

            # On ajoute le chemin à notre liste de succès
            processed_files.append(output_path)
            
            context.log.info(f"✅ Fichier sauvegardé : {output_path}")

    # --- ÉTAPE 4 : FIN ---

    # Si la liste est vide, on prévient qu'on n'a rien trouvé
    if not processed_files:
        context.log.warning("⚠️ Aucun fichier CSV trouvé dans le dossier inputs !")
    
    # On retourne la liste des fichiers créés
    return processed_files