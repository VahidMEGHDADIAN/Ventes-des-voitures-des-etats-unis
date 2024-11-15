import streamlit as st
import pandas as pd
import numpy as np

st.title('Ventes des voitures aux Etats-Unis')

df = pd.read_csv("car_prices_clean.csv")
# Charge le fichier CSV dans un DataFrame df.

st.dataframe(df)  # Same as st.write(df)

# Choisir la colonne pour le tri
colonne_tri = st.selectbox("Sélectionnez la colonne pour trier les données :", options=df.columns)
# Utilise un selectbox pour sélectionner une colonne pour le tri parmi celles de df

# Choisir l'ordre de tri (ascendant ou descendant)
ordre_tri = st.selectbox("Sélectionnez l'ordre de tri :", options=["Ascendant", "Descendant"])
# Propose de trier en "Ascendant" ou "Descendant".

# Si une colonne est sélectionnée, trier le DataFrame
if colonne_tri:
    # Utiliser sort_values avec l'ordre de tri choisi
    df = df.sort_values(by=colonne_tri, ascending=(ordre_tri == "Ascendant"))
    # Trie le DataFrame df selon la colonne et l'ordre sélectionnés.

# Afficher le DataFrame trié
st.dataframe(df)

# Convertir la colonne 'make' (marque_du_véhicule) en type catégoriel
df['make'] = df['make'].astype('category')
# Modifie la colonne make pour être de type category, ce qui permet de mieux gérer les valeurs pour les filtres.

# Initialisation de la DataFrame filtrée
df_filtre = df

# Filtrer les marques de véhicules
marques_disponibles = df['make'].cat.categories.tolist()  # Récupérer toutes les marques disponibles
marque_selectionnee = st.selectbox("Sélectionnez une marque de véhicule :", options=marques_disponibles)

# Filtrer le DataFrame en fonction de la marque sélectionnée
if marque_selectionnee:
    df_filtre = df_filtre[df_filtre['make'].isin([marque_selectionnee])]
    # Crée un selectbox pour sélectionner une marque de véhicule et filtre df_filtre selon cette sélection.

# Filtrer par année (exemple pour une colonne numérique)
if 'year' in df.columns:
    min_year, max_year = int(df['year'].min()), int(df['year'].max())
    year_range = st.slider("Sélectionnez la plage d'années :", min_value=min_year, max_value=max_year, value=(min_year, max_year))
    # Utilise un slider pour sélectionner une plage d'années et filtre df_filtre selon cette plage.

    # Filtrer le DataFrame en fonction de la plage d'années sélectionnée
    df_filtre = df_filtre[df_filtre['year'].between(year_range[0], year_range[1])]

# Filtrer par kilométrage (odometer)
if 'odometer' in df.columns:
    min_km, max_km = int(df['odometer'].min()), int(df['odometer'].max())
    odometer_range = st.slider("Sélectionnez la plage de kilométrage (odometer) :", min_value=min_km, max_value=max_km, value=(min_km, max_km))

    # Filtrer le DataFrame en fonction de la plage de kilométrage sélectionnée
    df_filtre = df_filtre[df_filtre['odometer'].between(odometer_range[0], odometer_range[1])]
    # Utilise un slider pour sélectionner une plage de kilométrage et filtre df_filtre en conséquence.

# Afficher le DataFrame final filtré
st.dataframe(df_filtre)

# Initialisation de la DataFrame filtrée
df_filtre = df.copy()

# Barre latérale pour les filtres
st.sidebar.header("Filtres")

# Itérer sur les colonnes pour créer des filtres automatiques dans la barre latérale
for col in df.columns:
    # Filtrage pour les colonnes catégorielles
    if pd.api.types.is_categorical_dtype(df[col]) or df[col].dtype == 'object':
        options = df[col].dropna().unique()  # Récupérer les valeurs uniques pour le filtre
        choix = st.sidebar.multiselect(f"Sélectionnez les valeurs pour '{col}' :", options=options)
        #Crée des filtres dynamiques pour chaque colonne :
        # Pour les colonnes catégorielles et textuelles (object), il propose un multiselect.
        # Pour les colonnes numériques, un slider.
        # Pour les colonnes de date, un date_input.

        # Filtrer si des valeurs sont sélectionnées
        if choix:
            df_filtre = df_filtre[df_filtre[col].isin(choix)]

    # Filtrage pour les colonnes numériques
    elif pd.api.types.is_numeric_dtype(df[col]):
        min_val = df[col].min()
        max_val = df[col].max()
        plage = st.sidebar.slider(f"Sélectionnez la plage pour '{col}' :", min_value=float(min_val), max_value=float(max_val), value=(float(min_val), float(max_val)))

        # Filtrer en fonction de la plage sélectionnée
        df_filtre = df_filtre[df_filtre[col].between(plage[0], plage[1])]

    # Filtrage pour les colonnes de type date
    elif pd.api.types.is_datetime64_any_dtype(df[col]):
        date_min = df[col].min()
        date_max = df[col].max()
        date_range = st.sidebar.date_input(f"Sélectionnez la plage pour '{col}' :", value=(date_min, date_max))

        # Filtrer si une plage de dates est sélectionnée
        if isinstance(date_range, tuple) and len(date_range) == 2:
            df_filtre = df_filtre[df[col].between(date_range[0], date_range[1])]

# Afficher la DataFrame filtrée dans la partie principale
st.header("Données filtrées")
st.dataframe(df_filtre)

# Fonction pour créer un fichier Excel à partir du DataFrame filtré
def to_excel(dataframe):
    # Convertir les colonnes catégorielles en chaînes de caractères
    for col in dataframe.select_dtypes(include='category').columns:
        dataframe[col] = dataframe[col].astype(str)
        
    # Sauvegarder directement le fichier Excel dans un fichier local
    excel_file = 'donnees_filtrees.xlsx'
    dataframe.to_excel(excel_file, index=False, sheet_name='Données Filtrées')
    return excel_file


# Bouton de téléchargement
excel_file = to_excel(df_filtre)  # Utiliser df_filtre ici, car il contient les données filtrées
st.download_button(
    label="Télécharger les données au format Excel",
    data=open(excel_file, 'rb'),  # Ouvrir le fichier Excel en mode binaire
    file_name='donnees_filtrees.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# Titre pour la fonctionnalité de groupement
st.title("Groupement des données")

# Interface utilisateur pour choisir la colonne de groupement
colonne_group = st.selectbox("Sélectionnez la colonne pour le groupement :", options=df.select_dtypes(include=['category', 'object']).columns)
# Sélectionne la colonne pour le groupement parmi les colonnes catégorielles et textuelles.

# Interface pour choisir les colonnes à agréger
# Sélectionner seulement les colonnes numériques pour l'agrégation
colonnes_numeriques = df.select_dtypes(include=['number']).columns.tolist()
colonnes_choisies = st.multiselect("Sélectionnez les colonnes numériques à agréger :", options=colonnes_numeriques)

# Interface pour choisir les fonctions d'agrégation
fonctions_agregation = ['sum', 'mean', 'min', 'max', 'count']
fonction_choisie = st.selectbox("Sélectionnez la fonction d'agrégation :", options=fonctions_agregation)
# Permet de choisir une fonction d'agrégation parmi sum, mean, min, max, et count.

# Vérifier que la fonction d'agrégation choisie est compatible avec les types de données
if colonne_group and colonnes_choisies:
    # Créer un dictionnaire d'agrégations basé sur les colonnes numériques et la fonction choisie
    aggregation_dict = {col: fonction_choisie for col in colonnes_choisies}

    # Appliquer groupby et l'agrégation
    try:
        df_grouped = df.groupby(colonne_group).agg(aggregation_dict)
        # Afficher le DataFrame groupé
        st.dataframe(df_grouped)
    except Exception as e:
        st.error(f"Erreur lors du groupement des données : {e}")
        # Utilise groupby pour grouper les données et appliquer la fonction d’agrégation sélectionnée.
