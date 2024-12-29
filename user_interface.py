import streamlit as st
from app.graphe import RechercheChemin

def creer_interface_utilisateur():
    st.set_page_config(page_title="Recherche de Chemin Dijkstra")
    
    st.title("Recherche de Chemin Dijkstra")
    
    # Sélection du type de graphe
    type_graphe = st.radio("Choisissez le type de graphe", 
                          ["Graphe Orienté", "Graphe Non Orienté"])
    
    # Initialiser le graphe en fonction du type choisi
    est_oriente = type_graphe == "Graphe Orienté"
    
    if 'recherche_chemin' not in st.session_state or st.session_state.est_oriente != est_oriente:
        st.session_state.recherche_chemin = RechercheChemin(est_oriente)
        st.session_state.est_oriente = est_oriente

    # Section Nœuds
    st.header("Ajouter des Nœuds")
    saisie_noeuds = st.text_input("Entrez les nœuds (séparés par des virgules)")
    if st.button("Ajouter Nœuds"):
        noeuds = [noeud.strip() for noeud in saisie_noeuds.split(',') if noeud.strip()]
        noeuds_ajoutes = st.session_state.recherche_chemin.ajouter_noeuds(noeuds)
        if noeuds_ajoutes:
            st.success(f"Nœuds ajoutés : {', '.join(noeuds_ajoutes)}")
        else:
            st.error("Aucun nœud n'a pu être ajouté.")

    # Section Arêtes
    st.header("Ajouter des Arêtes")
    saisie_aretes = st.text_area(f"Arêtes (format: NœudDépart,NœudArrivée,Poids)")
    if st.button("Ajouter Arêtes"):
        aretes = []
        for ligne in saisie_aretes.split('\n'):
            if ligne.strip():
                try:
                    noeud_depart, noeud_arrivee, poids = ligne.split(',')
                    aretes.append((noeud_depart.strip(), noeud_arrivee.strip(), float(poids.strip())))
                except ValueError:
                    st.error(f"Format d'arête incorrect : {ligne}")
                    continue
        
        aretes_ajoutees = st.session_state.recherche_chemin.ajouter_aretes(aretes)
        if aretes_ajoutees:
            st.success(f"Arêtes ajoutées : {aretes_ajoutees}")
        else:
            st.error("Aucune arête n'a pu être ajoutée. Vérifiez que les nœuds existent et que la direction est valide.")

    # Section Recherche de Chemin
    st.header("Trouver le Plus Court Chemin")
    noeuds = list(st.session_state.recherche_chemin.graphe.keys()) or ['']
    
    noeud_depart = st.selectbox("Nœud de départ", noeuds)
    noeud_arrivee = st.selectbox("Nœud d'arrivée", noeuds)

    if st.button("Trouver le Chemin"):
        chemin, distance_totale = st.session_state.recherche_chemin.dijkstra(noeud_depart, noeud_arrivee)
        
        if chemin:
            st.success(f"Chemin : {' → '.join(chemin)}")
            st.info(f"Distance totale : {distance_totale}")
            
            figure = st.session_state.recherche_chemin.dessiner_graphe(chemin)
            st.pyplot(figure)
        else:
            st.error("Aucun chemin trouvé entre ces nœuds.")

    # Graphe Actuel
    st.header("Graphe Actuel")
    st.json(st.session_state.recherche_chemin.graphe)

    # Bouton de Réinitialisation
    if st.button("Réinitialiser le Graphe"):
        st.session_state.recherche_chemin = RechercheChemin(est_oriente)
        st.rerun()

def interface_principale():
    creer_interface_utilisateur()