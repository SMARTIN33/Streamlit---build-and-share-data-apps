import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import random

# Charger le dataset
file_path = "cars_dataset.csv"

try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"Le fichier '{file_path}' est introuvable. Veuillez vérifier le chemin.")
    st.stop()

# Vérification de la colonne 'Region'
if 'Region' not in data.columns:
    st.warning("La colonne 'Region' n'existe pas. Une colonne fictive sera créée.")
    # Créer une colonne 'Region' avec des valeurs par défaut
    regions_default = ['US', 'Europe', 'Japon']
    data['Region'] = [random.choice(regions_default) for _ in range(len(data))]
    st.success("Colonne 'Region' fictive créée avec des valeurs aléatoires (US, Europe, Japon).")

# Titre de l'application
st.title("Analyse des Voitures : Corrélations et Distributions")
st.write("""
Cette application permet d'analyser les corrélations et distributions des données des voitures, 
avec la possibilité de filtrer par région (US / Europe / Japon).
""")

# Options de filtre par région
regions = data['Region'].unique()
selected_regions = st.multiselect("Sélectionnez les régions :", regions, default=regions)

# Filtrer les données par région
filtered_data = data[data['Region'].isin(selected_regions)]

# Vérification des données filtrées
if filtered_data.empty:
    st.warning("Aucune donnée disponible pour les régions sélectionnées.")
    st.stop()

# Analyse de corrélation
st.header("Analyse de Corrélation")
numeric_columns = filtered_data.select_dtypes(include=['float64', 'int64'])

if numeric_columns.empty:
    st.error("Aucune donnée numérique disponible pour l'analyse de corrélation.")
else:
    correlation_matrix = numeric_columns.corr()
    fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax_corr)
    ax_corr.set_title("Matrice de Corrélation")
    st.pyplot(fig_corr)
    st.write("La carte de chaleur ci-dessus montre les corrélations entre différentes variables dans les données filtrées.")

# Analyse de distribution
st.header("Analyse de Distribution")
if not numeric_columns.empty:
    for column in numeric_columns.columns:
        fig_dist, ax_dist = plt.subplots()
        sns.histplot(filtered_data[column], kde=True, ax=ax_dist)
        ax_dist.set_title(f"Distribution de {column}")
        st.pyplot(fig_dist)
else:
    st.warning("Aucune colonne numérique disponible pour l'analyse de distribution.")

# Exportation du script
st.write("L'application est prête à être déployée sur Streamlit. Téléchargez le script et publiez-le.")
