import streamlit as st
import matplotlib.pyplot as plt
from scripts.bank_analyst.script import get_list

# Affiche le fichier csv en prenant en compte les filtre datetime et label
# Affiche un graph en barres de la repartition des dépenses sur une période
def stats1():
    
    if 'data' in st.session_state:

        # Creation de deux colonnes et recuperation des data
        col1, col2 = st.columns(2, vertical_alignment="top")
        data_label_picked = st.session_state.data.copy()



        ########################################################################################
        # Colonne 1 : Champ de selection d'une enseigne, bouton d'activation du filtre 'only_in'
        # Apercu du tableau, si 'only_in' n'est pas activé, depenses et revenus sont présent
        with col1: 
            col1a,col1b = st.columns([1,1], vertical_alignment="bottom")

            # Menu déroulant - label
            with col1a:
                st.session_state.data_label = get_list(st.session_state.data, 'label')
                label_picked = st.selectbox("Selectionnez une enseigne (optionnel)", st.session_state.data_label, index=0)

            # Bouton toggle - 'only_in'
            with col1b:
                st.session_state.only_in = st.toggle("Selectionner uniquement les revennus")

            # Affichage du tableau avec 'only_in'
            if st.session_state.only_in:
                data_label_picked = data_label_picked[data_label_picked['type'] == 'TOPUP']
                st.dataframe(data_label_picked)

            # Affichage du tableau en mode normal
            # Filtre en fonction du label ou pas
            else:
                if label_picked:
                    data_label_picked = st.session_state.data[st.session_state.data['label'] == label_picked]
                    st.dataframe(data_label_picked)
                else:
                    st.dataframe(st.session_state.data)


        ###########################################################################
        # Colonne 2 : Graphe d'affichage des données présente dans le tableau joint
        # Affiche les sommes dépensés pour un label ou non, par années, mois ou jours

        # N'affiche les revenus que lorsque 'only_in' est activé (et seulement les revenus dans ce cas)
        # Si 'only_in' est desactivé :
        if not st.session_state.only_in:
            data_label_picked = data_label_picked[data_label_picked['type'] != 'TOPUP']
            data_label_picked['amount']= -data_label_picked['amount']

        period=''

        # Initialisation de la zone de graph
        fig, ax = plt.subplots(figsize=(10, 5))

        # Creation du diagrame a bar en fonction des filtres selectionnées
        if st.session_state.year:
            month_amount = data_label_picked.groupby(['month', 'month_id'])['amount'].sum().reset_index().sort_values('month_id')
            period='mois'
            ax.clear()
            ax.bar(month_amount['month'].astype(str), month_amount['amount'], color='skyblue')

            if st.session_state.month: 
                day_amount = data_label_picked.groupby(['day', 'day_id'])['amount'].sum().reset_index().sort_values('day_id')
                period='jours'
                ax.clear()
                ax.bar(day_amount['day'].astype(str), day_amount['amount'], color='skyblue')

                if st.session_state.day:
                    day_amount = data_label_picked.groupby(['day', 'day_id'])['amount'].sum().reset_index().sort_values('day_id')
                    period='jours'
                    ax.clear()
                    ax.bar(day_amount['day'].astype(str), day_amount['amount'], color='skyblue', width=0.1)
                    
        # Si aucun filtre n'est selectioné
        else:
            ax.clear()
            year_amount = data_label_picked.groupby(['year'])['amount'].sum().reset_index()
            ax.bar(year_amount['year'].astype(str), year_amount['amount'], color='skyblue')
            period='années'

        # Améliorations visuelles
        ax.set_xlabel(f'{period}')
        ax.set_ylabel('Montant total')
        ax.set_title(f'Montant total dépensé par {period}')
        ax.tick_params(axis='x', rotation=45)

        # Affichage sur la colonne, leger réalignement avec st.text("")
        with col2:
            for _ in range(4):
                st.text("")
            st.pyplot(fig)
