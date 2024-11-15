import pytest
import pandas as pd
import numpy as np
from io import BytesIO
from app_vahid import to_excel  # Assurez-vous que to_excel est dans votre fichier app_vahid.py

# Tester si le fichier CSV est bien chargé
def test_load_data():
    # Charger les données
    df = pd.read_csv("car_prices_clean.csv")
    assert not df.empty, "Le DataFrame ne doit pas être vide après le chargement des données."

# Tester le tri des données
@pytest.mark.parametrize("colonne, ordre, attendu", [
    ("year", "Ascendant", True),
    ("year", "Descendant", False)
])
def test_sort_data(colonne, ordre, attendu):
    df = pd.read_csv("car_prices_clean.csv")
    df = df.sort_values(by=colonne, ascending=(ordre == "Ascendant"))
    # Vérifier que le tri est dans le bon ordre
    assert (df[colonne].is_monotonic_increasing if attendu else df[colonne].is_monotonic_decreasing), "Le tri n'est pas correct."

# Tester le filtre par marque
def test_filter_make():
    df = pd.read_csv("car_prices_clean.csv")
    marque_test = df['make'].iloc[0]  # Choisir une marque pour le test
    df_filtre = df[df['make'] == marque_test]
    # Vérifier que toutes les lignes filtrées correspondent à la marque sélectionnée
    assert all(df_filtre['make'] == marque_test), "Le filtre de marque ne fonctionne pas correctement."

# Tester le filtre par année
def test_filter_year():
    df = pd.read_csv("car_prices_clean.csv")
    year_min, year_max = 2015, 2020
    df_filtre = df[df['year'].between(year_min, year_max)]
    # Vérifier que toutes les années sont dans la plage sélectionnée
    assert df_filtre['year'].between(year_min, year_max).all(), "Le filtre d'année ne fonctionne pas correctement."

# Tester le filtre par kilométrage
def test_filter_odometer():
    df = pd.read_csv("car_prices_clean.csv")
    min_km, max_km = 10000, 50000
    df_filtre = df[df['odometer'].between(min_km, max_km)]
    # Vérifier que le kilométrage est dans la plage sélectionnée
    assert df_filtre['odometer'].between(min_km, max_km).all(), "Le filtre de kilométrage ne fonctionne pas correctement."

# Tester la fonction de création de fichier Excel
def test_to_excel():
    df = pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": [4, 5, 6]
    })
    excel_file = to_excel(df)
    # Vérifier que le fichier existe et n'est pas vide
    with open(excel_file, 'rb') as f:
        data = f.read()
    assert data, "Le fichier Excel ne doit pas être vide."

# Tester la fonction de groupement
def test_groupby():
    df = pd.DataFrame({
        "make": ["Toyota", "Toyota", "Honda", "Honda"],
        "price": [20000, 25000, 18000, 22000]
    })
    df_grouped = df.groupby("make").agg({"price": "mean"})
    # Vérifier que le groupement produit les résultats attendus
    assert df_grouped.loc["Toyota", "price"] == 22500, "Le groupement pour Toyota est incorrect."
    assert df_grouped.loc["Honda", "price"] == 20000, "Le groupement pour Honda est incorrect."

# Tester le téléchargement du fichier Excel
def test_download_excel():
    df = pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": [4, 5, 6]
    })
    excel_file = to_excel(df)
    with open(excel_file, 'rb') as f:
        bytes_data = BytesIO(f.read())
    assert bytes_data.getvalue(), "Le fichier téléchargé ne doit pas être vide."


