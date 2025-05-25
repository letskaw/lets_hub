import streamlit as st
import matplotlib.pyplot as plt
from scripts.bank_analyst.script import get_list

def stats1():
    
    if 'data' in st.session_state:
        cols = st.columns(2, vertical_alignment="top")

        data_label_picked = st.session_state.data.copy()
        with cols[0]:

            ### Menu déroulant - label ###
            st.session_state.data_label = get_list(st.session_state.data, 'label')
            label = st.selectbox("Selectionnez une enseigne (optionnel)", st.session_state.data_label, index=0)

        
            if label:
                data_label_picked = st.session_state.data[st.session_state.data['label'] == label]
                st.dataframe(data_label_picked)
            else:
                st.dataframe(st.session_state.data)


        # Affichage des sommes dépensés pour un label ou non, par années, mois ou jours
        # Collecte de donnéees

        data_label_picked = data_label_picked[data_label_picked['type'] != 'TOPUP']
        data_label_picked['amount']= -data_label_picked['amount']
        period=''

        # Creation graph
        fig, ax = plt.subplots(figsize=(10, 5))

        # Creation du diagrame a bar en fonction des filtres selectionnées
        if st.session_state.year:
            month_amount = data_label_picked.groupby(['month', 'month_id'])['amount'].sum().reset_index().sort_values('month_id')
            ax.bar(month_amount['month'].astype(str), month_amount['amount'], color='skyblue')
            period='mois'
            if st.session_state.month:
                ax.clear()
                day_amount = data_label_picked.groupby(['day', 'day_id'])['amount'].sum().reset_index().sort_values('day_id')
                ax.bar(day_amount['day'].astype(str), day_amount['amount'], color='skyblue')
                period='jours'
                if st.session_state.day:
                    ax.clear()
                    day_amount = data_label_picked.groupby(['day', 'day_id'])['amount'].sum().reset_index().sort_values('day_id')
                    ax.bar(day_amount['day'].astype(str), day_amount['amount'], color='skyblue')
                    period='jours'

        else:
            year_amount = data_label_picked.groupby(['year'])['amount'].sum().reset_index()

            ax.bar(year_amount['year'].astype(str), year_amount['amount'], color='skyblue')
            period='années'

        # Améliorations visuelles
        ax.set_xlabel(f'{period}')
        ax.set_ylabel('Montant total')
        ax.set_title(f'Montant total dépensé par {period}')
        ax.tick_params(axis='x', rotation=45)

        with cols[1]:
            st.pyplot(fig)
