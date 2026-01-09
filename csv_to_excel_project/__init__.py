# Importation de l'objet principal 'Definitions' qui structure un projet Dagster
# et de la fonction utilitaire 'load_assets_from_modules'
from dagster import Definitions, load_assets_from_modules

# Importation de notre fichier 'assets.py' qui se trouve dans le même dossier (.)
from . import assets

# Cette fonction scanne automatiquement le fichier 'assets.py' pour trouver tout ce qui a un @asset
all_assets = load_assets_from_modules([assets])

# On crée l'objet Definitions qui est le point d'entrée de l'application Dagster
defs = Definitions(
    assets=all_assets,  # On lui donne la liste des assets qu'on a trouvés juste au-dessus
)