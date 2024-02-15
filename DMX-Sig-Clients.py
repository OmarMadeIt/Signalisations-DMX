import streamlit as st
import pandas as pd
from datetime import datetime
import os

#with st.sidebar:
     #path = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
     #for uploaded_file in path:
         #uploaded_file = pd.read_excel(uploaded_file)
            
#st.write(uploaded_file.head())

#st.write(uploaded_file.shape)
#@st.cache_data

def charger_fichiers_excel(files):
    df_list = []
    for file in files:
        df_temp = pd.read_excel(file)
        df_temp['Fichier_source'] = os.path.basename(file.name)
        df_list.append(df_temp)
    final_dataframe = pd.concat(df_list, ignore_index=True)
    
    #final_dataframe.to_csv("Base_Globale_OeM_Mensuel.csv", index=False, sep=',')
    print(final_dataframe.head())
    print(f"Le dataframe comporte: {final_dataframe.shape}")
    final_dataframe.columns = [c.replace(' ', '_') for c in final_dataframe.columns]
    print(final_dataframe.head())
    df_repliq = final_dataframe.copy()
    df_repliq['Créé_le']=pd.to_datetime(df_repliq['Créé_le'], format ='%y-%m-%d %H:%M:%S')
    df_repliq['Date_Appel'] = df_repliq['Créé_le'].dt.strftime('%d/%m/%Y')
    df_repliq['Date_Appel_Mois'] = df_repliq['Créé_le'].dt.strftime('%Y-%m')
    #df_repliq=df_repliq.loc[(df_repliq['Créé_le']>=date_debut)&(df_repliq['Créé_le']<date_fin)]
    print(f"Le dataframe final comporte: {df_repliq.shape}")
    df_repliq['Motif']=df_repliq['Motif'].str.lower()
    df_repliq['Motif']=df_repliq['Motif'].str.strip()
    df_repliq['Motif']=df_repliq["Motif"].str.rsplit("-", 1).str[-1]
    df_repliq['Motif']=df_repliq['Motif'].str.strip()
    #output_globale = df_repliq.groupby(by=['Date_Appel_Mois', 'Motif','Type_Offre','CaseConfirmer'],as_index=False).agg({'Numéro_du_case':'count', 'Numéro_Appelant':'nunique'})
    #output_globale.rename(columns={'Numéro_du_case':'Nb_Signalisations', 'Numéro_Appelant':'Nb_Appelants', 'CaseConfirmer':'Statut_Cas'}, inplace=True)
    #output_globale.to_csv(r'C:\Users\seck028732\Documents\CBM\CBM\OSN\DMX\Final\base_ref_output_new_'+mois+'.csv', sep=';', encoding='utf-8-sig', index=False)
    return df_repliq

# Interface utilisateur avec Streamlit
st.title("Importation de fichiers Excel")

# Sélection des fichiers Excel à charger
uploaded_files = st.file_uploader("Uploader les fichiers Excel", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    # Bouton pour charger les fichiers sélectionnés
    #if st.button("Charger les fichiers"):
        # Charger les fichiers Excel et concaténer les DataFrames
    df_final = charger_fichiers_excel(uploaded_files)

    # Afficher les premières lignes du DataFrame final
    st.write("Aperçu des données :")
    st.write(df_final.head())
    st.write(df_final.shape)
    #st.write(df_final.groupby(['Motif'])['Numéro_du_case'].count())


# Filtrer sur les colonnes de dates
start_date = st.date_input("Date de début", value=None)
end_date = st.date_input("Date de fin", value=None)

if st.button('Soumettre'):
    if start_date is not None and end_date is not None:
        start_date = pd.to_datetime(start_date).date()
        end_date = pd.to_datetime(end_date).date()

        #df_final['Date_Appel'] = pd.to_datetime(df_final['Date_Appel'], format='%Y-%m-%d')
        df_final['Date_Appel'] = pd.to_datetime(df_final['Date_Appel'], format='%d/%m/%Y')
    if start_date is not None and end_date is not None:
        df_final = df_final[
            (pd.to_datetime(df_final['Date_Appel']).dt.date >= start_date)
            & (pd.to_datetime(df_final['Date_Appel']).dt.date <= end_date)
        ]
    output_globale = df_final.groupby(by=['Date_Appel_Mois', 'Motif','Type_Offre','CaseConfirmer'],as_index=False).agg({'Numéro_du_case':'count', 'Numéro_Appelant':'nunique'})
    output_globale.rename(columns={'Numéro_du_case':'Nb_Signalisations', 'Numéro_Appelant':'Nb_Appelants', 'CaseConfirmer':'Statut_Cas'}, inplace=True)


    #st.write(output_globale.head())
    st.write(output_globale.head())
            # Bouton pour exporter le DataFrame en CSV
    st.download_button(
       "Télécharger le fichier",
       output_globale.to_csv(index=False, sep=';', encoding='latin-1'),
       "file.csv",
       "text/csv",
       key='download-csv'
    )
