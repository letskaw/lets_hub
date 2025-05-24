import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd



########################################################################
########################
### DATA & GRAPH 02 ###     sommes dépensées par enseigne

def stats2():
    if 'data' in st.session_state:
        data = st.session_state.data

        data_all_labels= data[data['type'] != 'TOPUP']
        data_all_labels['amount']= -data_all_labels['amount']
        st.subheader("Somme par enseigne")
        data_all_labels = (data_all_labels.groupby(['label'])['amount'].sum().reset_index()).sort_values(['amount'], ascending=False)
        st.dataframe(data_all_labels)


        # Affichage du graphique sommes dépensées par enseigne
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(data_all_labels['label'].iloc[:10], data_all_labels['amount'].iloc[:10], color='skyblue')

        # Améliorations visuelles
        ax.set_xlabel("Enseigne")
        ax.set_ylabel("Montant total")
        ax.set_title("Montant total dépensé par enseigne")
        ax.tick_params(axis='x', rotation=45)

        st.pyplot(fig)
    else:
        st.subheader("❌     Aucun fichier csv chargé     ❌")

stats2()