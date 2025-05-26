import streamlit as st
import matplotlib.pyplot as plt

# Affiche les dépenses dans les differentes enseignes classé par sommes decroissantes
# Affiche un graph en barres des 10 enseigne avec les plus grosse dépenses
def stats2():

    col1, col2 = st.columns(2, vertical_alignment="top")


    if 'data' in st.session_state:
        data = st.session_state.data

        data_all_labels= data[data['type'] != 'TOPUP']
        data_all_labels['amount']= -data_all_labels['amount']
        data_all_labels = (data_all_labels.groupby(['label'])['amount'].sum().reset_index()).sort_values(['amount'], ascending=False)
        
        with col1:
            st.dataframe(data_all_labels)
        # Affichage du graphique sommes dépensées par enseigne
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(data_all_labels['label'].iloc[:10], data_all_labels['amount'].iloc[:10], color='skyblue')

        # Améliorations visuelles
        ax.set_xlabel("Enseigne")
        ax.set_ylabel("Montant total")
        ax.set_title("Montant total dépensé par enseigne")
        ax.tick_params(axis='x', rotation=45)

        with col2:
            st.pyplot(fig)
