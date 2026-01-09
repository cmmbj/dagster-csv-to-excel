# Importation du module 'os' pour naviguer dans les dossiers et gérer les noms de fichiers
import os

# Importation de Pandas pour la manipulation des données
import pandas as pd

# Importation des outils Dagster
from dagster import asset, AssetExecutionContext

@asset
def convert_all_csvs(context: AssetExecutionContext):
    """
    Asset robuste : convertit les CSV en Excel et gère les erreurs
    sans arrêter le processus complet.
    """
    
    # --- ÉTAPE 1 : DÉFINITION DES DOSSIERS ---
    current_dir = os.path.dirname(__file__)
    inputs_folder = os.path.join(current_dir, "data", "inputs")
    outputs_folder = os.path.join(current_dir, "data", "outputs")

    # --- ÉTAPE 2 : LISTER LES FICHIERS ---
    all_files = os.listdir(inputs_folder)
    
    # Listes pour le rapport final
    processed_files = []
    failed_files = [] 

    # --- ÉTAPE 3 : LA BOUCLE AVEC SÉCURITÉ ---
    for filename in all_files:
        if filename.endswith(".csv"):
            
            # Chemins
            input_path = os.path.join(inputs_folder, filename)
            file_root_name = os.path.splitext(filename)[0]
            new_filename = file_root_name + ".xlsx"
            output_path = os.path.join(outputs_folder, new_filename)

            context.log.info(f"🔄 Tentative de traitement : {filename}")

            # >>> DÉBUT DE LA ZONE PROTÉGÉE <<<
            try:
                # 1. On essaie de lire le CSV
                # C'est ici que 'bad_data.csv' va déclencher une alerte, mais pas un crash
                df = pd.read_csv(input_path)
                
                # Petite vérification supplémentaire si le fichier est vide
                if df.empty:
                    raise ValueError("Le fichier est vide")

                # 2. On écrit le fichier Excel
                df.to_excel(output_path, index=False)
                
                # 3. Si on arrive ici, c'est que tout s'est bien passé
                context.log.info(f"✅ Succès : {new_filename}")
                processed_files.append(output_path)

            except Exception as e:
                # >>> ZONE DE GESTION D'ERREUR <<<
                # Si n'importe quoi se passe mal au-dessus, on atterrit ici.
                error_message = f"❌ ÉCHEC sur {filename}. Raison : {str(e)}"
                
                # On note l'erreur en rouge dans les logs
                context.log.error(error_message)
                
                # On ajoute le fichier à la liste des échecs pour le bilan
                failed_files.append(filename)
            
            # >>> FIN DE LA ZONE PROTÉGÉE <<<

    # --- ÉTAPE 4 : BILAN FINAL ---
    
    # On affiche un résumé clair dans les logs
    if failed_files:
        context.log.warning(f"⚠️ Terminé avec des erreurs. Fichiers échoués ({len(failed_files)}) : {failed_files}")
    else:
        context.log.info("🎉 Tous les fichiers ont été traités sans aucune erreur.")

    # On retourne la liste des fichiers réussis
    return processed_files