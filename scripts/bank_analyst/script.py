import pandas as pd
from babel.dates import format_date
import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import io

#
#
#
#
#
#
#
#############################################
########## LOAD & GET_LIST ##########
#############################################

# Retourne un dataframe à partir un d'un fichier csv de la banque Revolut
# Mets à jour le format des valeures et le nom 
def load_data(file_csv):

    data = pd.read_csv(file_csv)

    # Reformatage des données
    data['Amount'] = data['Amount'].astype(float)
    data['Started Date'] = pd.to_datetime(data['Started Date'])
    data['year'] = data['Started Date'].dt.year
    data['day'] = data['Started Date'].apply(lambda x: format_date(x, format='EEEE', locale='fr_FR')).str.capitalize() + ' ' + data['Started Date'].dt.day.astype(str)
    data['day_id'] = data['Started Date'].dt.day
    data['month'] = data['Started Date'].apply(lambda x: format_date(x, format='MMMM', locale='fr_FR')).str.capitalize()
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

# Initialise les variable globale stocké dans session_state
def lets_init_session_state():
    st.session_state.data = st.session_state.data_origins
    st.session_state.list_year = []
    st.session_state.list_month = []
    st.session_state.list_day = []
    st.session_state.label_picked = ""
    st.session_state.only_in = None
    st.session_state.init_session = True
    st.session_state.segmented_picked = "Données globale"
    st.session_state.already_advert = False
#
#
#
#
#
#
#
#############################################
########## PREMIER ONGLET DE STATS ##########
#############################################

def get_df1(label_picked=None):
    data_label_picked = st.session_state.data.copy()


    # Affichage du tableau avec 'only_in'
    if st.session_state.only_in:
        data_label_picked = data_label_picked[data_label_picked['type'] == 'TOPUP']
        return data_label_picked[['label', 'amount', 'day', 'month', 'year']]

    # Affichage du tableau en mode normal
    # Filtre en fonction du label ou pas
    else:
        if label_picked:
            data_label_picked = data_label_picked[data_label_picked['label'] == label_picked]
            return data_label_picked[['label', 'amount', 'day', 'month', 'year']]
        
        return st.session_state.data[['label', 'amount', 'day', 'month', 'year']]
    
def get_df1_title():
    if st.session_state.label_picked and st.session_state.year:
        return st.text(f' Dépenses en {st.session_state.month} {st.session_state.year} chez {st.session_state.label_picked}')
    elif st.session_state.label_picked and not st.session_state.year:
        return st.text(f' Dépenses chez {st.session_state.label_picked}')
    elif not st.session_state.label_picked and not st.session_state.year:
        return st.text(f' Relevé de compte sans filtres')
    else:
        return st.text(f' Liste des dépenses en {st.session_state.month} {st.session_state.year}')

def get_fig1(label_picked=None):
    if "data" in st.session_state:
        data_label_picked = st.session_state.data.copy()

        if st.session_state.only_in:
            data_label_picked = data_label_picked[data_label_picked['type'] == 'TOPUP']
        else :
            data_label_picked = data_label_picked[data_label_picked['type'] != 'TOPUP']
            data_label_picked ['amount']= -data_label_picked['amount']
            
            if label_picked:
                data_label_picked  = data_label_picked[data_label_picked['label']==label_picked]

        period=''
        # Initialisation de la zone de graph
        fig, ax = plt.subplots(figsize=(10, 5))

        # Creation du diagrame a bar en fonction des filtres selectionnées
        if "year" in st.session_state and st.session_state.year:
            month_amount = data_label_picked.groupby(['month', 'month_id'])['amount'].sum().reset_index().sort_values('month_id')
            period='mois'
            ax.clear()
            ax.bar(month_amount['month'].astype(str), month_amount['amount'], color="#006666")

            if "month" in st.session_state and st.session_state.month : 
                day_amount = data_label_picked.groupby(['day', 'day_id'])['amount'].sum().reset_index().sort_values('day_id')
                period='jours'
                ax.clear()
                ax.bar(day_amount['day'].astype(str), day_amount['amount'], color="#006666")

                if "day" in st.session_state and st.session_state.day:
                    day_amount = data_label_picked.groupby(['day', 'day_id'])['amount'].sum().reset_index().sort_values('day_id')
                    period='jours'
                    ax.clear()
                    ax.bar(day_amount['day'].astype(str), day_amount['amount'], color="#006666", width=0.1)
                    
        # Si aucun filtre n'est selectioné
        else:
            ax.clear()
            year_amount = data_label_picked.groupby(['year'])['amount'].sum().reset_index()
            ax.bar(year_amount['year'].astype(str), year_amount['amount'], color="#006666")
            period='années'

        # Améliorations visuelles
        ax.set_xlabel(f'{period}')
        ax.set_ylabel('Montant total')

        if st.session_state.label_picked and st.session_state.year:
            ax.set_title(f' Representation des dépenses par {period} en {st.session_state.month} {st.session_state.year} chez {st.session_state.label_picked}')
        elif st.session_state.label_picked and not st.session_state.year:
            ax.set_title(f' Representation des dépenses par {period} chez {st.session_state.label_picked}')
        elif not st.session_state.label_picked and not st.session_state.year:
            ax.set_title(f' Representation des dépenses par {period}')
        else:
            ax.set_title(f'Representation des dépenses par {period} en {st.session_state.month} {st.session_state.year}')
        ax.tick_params(axis='x', rotation=45)


        return fig
#
#
#
#
#
#
#
##############################################
########## DEUXIEME ONGLET DE STATS ##########
##############################################
def get_df2():
  
    data = st.session_state.data_without_label.copy()

    data= data[data['type'] != 'TOPUP']
    data['amount']= -data['amount']
    data= (data.groupby(['label'])['amount'].sum().reset_index()).sort_values(['amount'], ascending=False)
    
    return data

def get_df2_title():
    if st.session_state.year:
        return st.text(f'Classement des enseigne par total de dépenses en {st.session_state.month} {st.session_state.year}')
    else:
        return st.text(f'Classement des enseigne par total de dépenses')   

def get_fig2():

    data = st.session_state.data_without_label.copy()

    data= data[data['type'] != 'TOPUP']
    data['amount']= -data['amount']
    data= (data.groupby(['label'])['amount'].sum().reset_index()).sort_values(['amount'], ascending=False)
    

    # Affichage du graphique sommes dépensées par enseigne
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(data['label'].iloc[:10], data['amount'].iloc[:10], color="#006666")

    # Améliorations visuelles
    ax.set_xlabel("Enseigne")
    ax.set_ylabel("Montant total")
    if st.session_state.year:
        ax.set_title(f"Representation du TOP 10 des enseigne par total de dépenses en {st.session_state.month} {st.session_state.year}")
    else:
        ax.set_title(f"Representation du TOP 10 des enseigne par total de dépenses")

    ax.tick_params(axis='x', rotation=45)

    return fig
#
#
#
#
#
#
#
######################################
########## GESTION DES PDFs ##########
######################################
def add_page_to_pdf(pdf):

    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Compte Rendu - Let's Hub", ln=True, align="C")


def add_fig_to_pdf(pdf, fig):

    img_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig.savefig(img_temp.name, bbox_inches='tight')
    plt.close(fig)
    pdf.image(img_temp.name, x=10, w=180)


def add_df_to_pdf(pdf, df, max_rows=10):
    pdf.set_font("Arial", size=10)

    if df.empty:
        pdf.cell(200, 10, "Aucune donnée à afficher.", ln=True)
        return

    # Définir largeur de colonnes proportionnelle
    col_count = len(df.columns)
    table_width = pdf.w - 20  # 10 mm de marge de chaque côté
    col_width = table_width / col_count

    # En-têtes
    pdf.set_fill_color(200, 200, 200)
    for col in df.columns:
        pdf.cell(col_width, 8, str(col), border=1, fill=True)
    pdf.ln()

    # Lignes de données
    for _, row in df.head(max_rows).iterrows():
        for cell in row:
            pdf.cell(col_width, 8, str(cell), border=1)
        pdf.ln()


def get_pdf(check_list):
    from scripts.bank_analyst.script import get_df1, get_df2, get_fig1, get_fig2

    # Creation du PDF
    pdf = FPDF()

    # Ajout page 1
    add_page_to_pdf(pdf)
    pdf.ln()
    
    # Figure 1, depenses par date et/ou enseigne
    if check_list[1]:
        add_fig_to_pdf(pdf, get_fig1())
        pdf.ln()
        

    #Figure 2, comparaison des 10 plus grosses depenses chez les differentes enseignes 
    if check_list[3]:
        add_fig_to_pdf(pdf, get_fig2())
        pdf.ln()

    # Ajout page 2
    #add_page_to_pdf(pdf)

    # Dataframe 1, Tableau global
    if check_list[0]:
        add_df_to_pdf(pdf, get_df1(), max_rows=1000)
        pdf.ln()

    # Dataframe 2, comparaison des plus grosses depenses chez les differentes enseignes 
    if check_list[2]:
        add_df_to_pdf(pdf, get_df2(), max_rows=1000)
        pdf.ln()

    # Transforme le PDF sous forme de bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')  # important: encode le string en bytes

    return io.BytesIO(pdf_bytes)
#
#
#
#
#
#
#
######################################
######### POP UP - DOWNLOAD ##########
######################################
@st.dialog("PDF Downloader")
def show_pdf_popup(tab):
    st.write(f"Que voulez vous inclure dans votre rapport ?")
    col1, col2 = st.columns(2, vertical_alignment="center")
    check_list = []

    # Ligne 1
    with col1:
        st.text(f"{tab[0]}")
    with col2:
        col2a, col2b = st.columns(2, vertical_alignment="center")
        with col2a:
            tab1_df_check = st.checkbox(f":material/table: !", key=1)
            check_list.append(tab1_df_check)
        with col2b:
            tab1_fig_check = st.checkbox(f":material/finance:", key=2, value= True)
            check_list.append(tab1_fig_check)

    # Ligne 2
    with col1:
        st.text(f"{tab[1]}")
    with col2:
        col2a, col2b = st.columns(2, vertical_alignment="center")
        with col2a:
            tab2_df_check = st.checkbox(f":material/table:", key=3, value=False)
            check_list.append(tab2_df_check)
        with col2b:
            tab2_fig_check = st.checkbox(f":material/finance:",key=4, value=True)
            check_list.append(tab2_fig_check)


    st.markdown(" ! :material/warning: Fichiers volumineux :material/warning:")
    pdf = get_pdf(check_list)
    st.download_button(":material/download: Download", pdf, "compte_rendu.pdf", "application/pdf", type="secondary", use_container_width=True)
#
#
#
#
#
#
#
######################################
############ MENU DE TRI #############
######################################
def get_sort_menu():

    st.session_state.data = st.session_state.data_origins.copy()
    st.session_state.data_without_label = st.session_state.data

    only_in = st.checkbox("Entrées d'argent")
    st.session_state.only_in = only_in
    

    if not only_in:
        ### Menu déroulant - Label ###
        st.session_state.list_label = get_list(st.session_state.data, 'label')
        st.session_state.list_label = sorted(st.session_state.list_label) 
        st.session_state.label_picked = st.selectbox("Enseigne", st.session_state.list_label, index=0)

        if st.session_state.label_picked :
            st.session_state.data = st.session_state.data[st.session_state.data['label'] == st.session_state.label_picked]
            
    ### Menu déroulant - year ###
    st.session_state.list_year = get_list( st.session_state.data, 'year')
    st.session_state.year = st.selectbox("Années", st.session_state.list_year, index=0)

    if st.session_state.year:
        st.session_state.data = st.session_state.data[st.session_state.data['year'] == st.session_state.year]
        st.session_state.data_without_label = st.session_state.data_without_label[st.session_state.data_without_label['year'] == st.session_state.year]

    ### Menu déroulant - month ###
    st.session_state.list_month  = get_list(st.session_state.data, 'month')
    st.session_state.month = st.selectbox("Mois", st.session_state.list_month, index=0)

    if st.session_state.month:
        st.session_state.data = st.session_state.data[st.session_state.data['month'] == st.session_state.month]
        st.session_state.data_without_label = st.session_state.data_without_label[st.session_state.data_without_label['month'] == st.session_state.month]

        ### Menu déroulant - day ###
        st.session_state.list_day= get_list(st.session_state.data, 'day')
        '''st.session_state.day = st.selectbox("Jour", st.session_state.list_day, index=0)

        if st.session_state.day:
            st.session_state.data = st.session_state.data[st.session_state.data['day'] == st.session_state.day]
            st.session_state.data_without_label = st.session_state.data_without_label[st.session_state.data['day'] == st.session_state.day]'''
#
#
#
#
#
#
#
######################################
########## AUTRES FONCTIONS ##########
######################################
'''def get_stats1_inputs():     
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    st.session_state.data_label = get_list(st.session_state.data, 'label')

    with col1:
        label_picked = st.selectbox("Selectionnez une enseigne (optionnel)", st.session_state.data_label, index=0)
    with col2:
        only_in = st.toggle("Selectionner uniquement les revennus entrants")
        st.session_state.only_in = only_in

    return label_picked, only_in'''

'''def get_total_amount(label):
    data = pd.df(st.session_state.data)
    return data.groupby([label])["amount"].sum()


    

def show_metrics():
    col1, col2, col3 = st.columns(3)

    if st.session_state.label_picked and st.session_state.year:
        name = f"Total des dépenses en {st.session_state.month} {st.session_state.year} chez {st.session_state.label_picked}"
        if st.session_state
        col1.metric(name, get_total_amount())

    elif st.session_state.label_picked and not st.session_state.year:
        name = f'Total des dépenses chez {st.session_state.label_picked}'
        col1.metric(name, get_total_amount())

    elif not st.session_state.label_picked and not st.session_state.year:
        name = f'Total des dépenses'
        col1.metric(name, get_total_amount())

    else:
        name = f'Total des dépenses en {st.session_state.month} {st.session_state.year}'
        col1.metric(name, get_total_amount())

'''


























"""                
                col1a, col1b = st.columns(2, vertical_alignment="bottom")
                st.session_state.data_label = get_list(st.session_state.data, 'label')

                with col1a:
                    label_picked = st.selectbox("Selectionnez une enseigne (optionnel)", st.session_state.data_label, index=0)
                with col1b:
                    st.session_state.only_in = st.toggle("Selectionner uniquement les revennus entrants")
"""





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