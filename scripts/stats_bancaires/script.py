import pandas as pd
from babel.dates import format_date


# Retourne un dataframe à partir un d'un fichier csv de la banque Revolut
# Mets à jour le format des valeures et le nom 
def load_data(file_csv):

    data = pd.read_csv(file_csv)

    # Reformatage des données
    data['Amount'] = data['Amount'].str.replace(',', '.', regex=False).astype(float)
    data['Started Date'] = pd.to_datetime(data['Started Date'])
    data['year'] = data['Started Date'].dt.year
    data['day'] = data['Started Date'].apply(lambda x: format_date(x, format='MMMM', locale='fr_FR')) + ' ' + data['Started Date'].dt.day.astype(str)
    data['day_id'] = data['Started Date'].dt.day
    data['month'] = data['Started Date'].apply(lambda x: format_date(x, format='MMMM', locale='fr_FR'))
    data['month_id'] = data['Started Date'].dt.month


    data = data[['Description', 'Amount', 'day','day_id', 'month', 'month_id', 'year', 'Type']]
    new_labels = ['label', 'amount', 'day','day_id', 'month', 'month_id', 'year', 'type']

    for i, new_label in enumerate(new_labels):
        old_label = data.columns.values[i]
        if old_label!=new_label:
            data.rename(columns={old_label : new_label}, inplace=True)


    return data


# Retourne la liste des elements differents present dans une colonne
def get_list(data, label1, label2=None):
    
    if label2:
        # Concatène deux Series puis filtre les doublons et NaN
        data['label_concat']= data[label1]+str(data[label2])
        return data
    

    return [''] + data[label1].dropna().unique().tolist()



'''new_labels = ['type', 'year', 'month', 'day', 'label', 'amount']

if len(data_bq_exploit.columns.values) == len(new_labels):
    for i, new_label in enumerate(new_labels):
        old_label = data_bq_exploit.columns.values[i]
        data_bq_exploit.rename(columns={old_label : new_label}, inplace=True)


'''
'''mask_cafe = data['Description']=='DIS\'Automatic'
mask_papaia = data['Description']=='Papaia'

 


sum_per_desc = data.groupby(['Description'])['Amount'].sum().reset_index()
sum_per_desc_date = data.groupby(['year', 'Mois', 'Description'])['Amount'].sum().reset_index()

'''


'''machine_cafe_cout_mois = machine_cafe_cout.groupby(['year_Mois'])['Amount'].sum().reset_index()
machine_cafe_cout_total = machine_cafe_cout.groupby(['Description'])['Amount'].sum().reset_index()
'''
'''data_bq_exploit.sort_values(['year', 'month']).to_csv('res.csv')
print('oh yeah')
'''






### EXEMPLE D'IHM BY GPT ###
"""st.title("Analyse de mes dépenses")

# Upload d'un fichier CSV
uploaded_file = st.file_uploader("Choisir un fichier CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Aperçu du fichier")
    st.dataframe(df)

    # Sélection de colonnes pour un graphique
    col_x = st.selectbox("Colonne X", df.columns)
    col_y = st.selectbox("Colonne Y", df.columns)

    # Affichage du graphique
    fig, ax = plt.subplots()
    df.groupby(col_x)[col_y].sum().plot(kind='bar', ax=ax)
    st.pyplot(fig)

    # Export CSV
    st.download_button("Télécharger les données", df.to_csv(index=False), "resultat.csv", "text/csv")

"""

"""mon_projet/
│
├── analyse.py          ← ici tu mets tes fonctions d’analyse (Pandas, Matplotlib, etc.)
└── app.py              ← ici tu mets l’IHM Streamlit qui appelle analyse.py

🔧 1. analyse.py — les fonctions

import pandas as pd

def charger_donnees(fichier_csv):
    return pd.read_csv(fichier_csv)

def total_par_mois(df):
    return df.groupby(['Annee', 'Mois'])['Amount'].sum().reset_index()

def filtrer_par_mot_cle(df, mot):
    return df[df['Description'].str.contains(mot, case=False, na=False)]

🖥 2. app.py — l’IHM

import streamlit as st
import matplotlib.pyplot as plt
from analyse import charger_donnees, total_par_mois, filtrer_par_mot_cle

st.title("Analyse des dépenses bancaires")

fichier = st.file_uploader("Importer un fichier CSV", type="csv")
if fichier:
    df = charger_donnees(fichier)
    st.dataframe(df)

    mot_cle = st.text_input("Filtrer par mot-clé (description)")
    if mot_cle:
        df = filtrer_par_mot_cle(df, mot_cle)

    st.subheader("Dépenses totales par mois")
    df_total = total_par_mois(df)

    fig, ax = plt.subplots()
    df_total.plot(x='Mois', y='Amount', kind='bar', ax=ax)
    st.pyplot(fig)

    st.download_button("Télécharger les données filtrées", df.to_csv(index=False), "filtre.csv", "text/csv")
"""


'''def test():
    data_test_tosort = load_data_revolut('csv/revolut_releve.csv')


    #print([""]+get_list(data_revolut, 'label'))

    data_test_tosort = data_test_tosort[data_test_tosort['month_id'] == 10]
    data_test_tosort['concat'] = data_test_tosort['day']+' '+data_test_tosort['day_id'].astype(str)
    
    print(data_test_tosort)
    #data_test = get_list(data_test_tosort, 'day', 'day_id')
    #print(data_test)
    #data_test = ['']
    #print(data_revolut_day_tosort)
    

    print(data_test)

test()'''