import pandas as pd
import streamlit as st


############            Data          ################

df0=pd.read_csv("car_prices_clean.csv")
df = df0.copy()

############            Types          ################
def formatTypes(df: pd.DataFrame):
    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]):  
            df[col]=df[col].astype('category')
        if 'date' in col:
            df[col] = pd.to_datetime(df[col])
            df[col] = df[col].dt.tz_localize(None)
    return df

############            Filter          ################


def filter(df: pd.DataFrame) -> pd.DataFrame:   

    with st.sidebar:
        left, right = st.columns((1, 20))
        for col in df.columns:
        

            if pd.api.types.is_numeric_dtype(df[col]):            
                minVal=float(df[col].min())
                maxVal=float(df[col].max())
                step=(maxVal-minVal)/100
                slider=right.slider(
                            label=f"Select range for {col}", 
                            #key=f"{col}Slider", 
                            min_value=minVal,
                            max_value=maxVal,
                            value=(minVal,maxVal),
                            step=1.0
                            )
                df=df[df[col].between(slider[0],slider[1])]


            elif isinstance(df[col].dtype, pd.CategoricalDtype):
                uniqueValues=df[col].unique()
                selectedValues=right.multiselect(f"Select {col} ",uniqueValues)
                if  selectedValues: 
                    df=df[df[col].isin(selectedValues)]          
            
            

            elif pd.api.types.is_datetime64_any_dtype(df[col]):           
                dateStart=df[col].min()
                dateEnd=df[col].max()
                dateRange=right.date_input(f"Select range of {col}", [dateStart,dateEnd])
                if dateRange:
                    df= df.loc[df[col].between(pd.to_datetime(dateRange[0]), pd.to_datetime(dateRange[1]))]
        return df
#########################################################



############            Sort          ################

def sort(df: pd.DataFrame) -> pd.DataFrame:
    sortColumn=st.selectbox(label="Choose the column",
                        options=[None]+list(df.columns),                    
                        format_func=lambda x: "Select to sort" if x is None else x)
    if  sortColumn is not None:
        sortOrder = st.radio("Choose sorting order:", ("Ascending", "Descending"))
        ascending = True if sortOrder == "Ascending" else False
        
        st.markdown(f"<p style='font-size:15px;'>The table sorted by {sortColumn}</p>",
                    unsafe_allow_html=True)
        df=df.sort_values(by=sortColumn,ascending=ascending)  
    return df
#########################################################

############            Display          ################

st.set_page_config( layout="wide" )
st.title("Car Sales In the USA")
st.sidebar.title("Filter")
st.dataframe(sort((filter(formatTypes(df))))) 
#st.sidebar.title("Group By")

#########################################################


############            Export           ################

st.download_button(
                label = "Export", 
                data = df.to_csv().encode("utf-8"),
                file_name = "dataframe.csv",
                mime = "text/csv"
                )

#########################################################

# Titre pour la fonctionnalité de groupement
st.title("Groupement des données")

# Interface utilisateur pour choisir la colonne de groupement
colonne_group = st.selectbox("Sélectionnez la colonne pour le groupement :", options=df.select_dtypes(include=['category', 'object']).columns)

# Interface pour choisir les colonnes à agréger
# Sélectionner seulement les colonnes numériques pour l'agrégation
colonnes_numeriques = df.select_dtypes(include=['number']).columns.tolist()
colonnes_choisies = st.multiselect("Sélectionnez les colonnes numériques à agréger :", options=colonnes_numeriques)

# Interface pour choisir les fonctions d'agrégation
fonctions_agregation = ['sum', 'mean', 'min', 'max', 'count']
fonction_choisie = st.selectbox("Sélectionnez la fonction d'agrégation :", options=fonctions_agregation)

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
