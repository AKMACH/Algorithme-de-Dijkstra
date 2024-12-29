import heapq
import networkx as nx
import matplotlib.pyplot as plt

class RechercheChemin:
    def __init__(self, est_oriente=True):
        self.graphe = {}
        self.est_oriente = est_oriente

    def ajouter_noeud(self, noeud):
        if noeud and noeud not in self.graphe:
            self.graphe[noeud] = {}
            return True
        return False

    def ajouter_noeuds(self, liste_noeuds):
        noeuds_ajoutes = []
        for noeud in liste_noeuds:
            if self.ajouter_noeud(noeud):
                noeuds_ajoutes.append(noeud)
        return noeuds_ajoutes

    def ajouter_arete(self, noeud_depart, noeud_arrivee, poids):
        # Vérifier si les nœuds existent
        if noeud_depart not in self.graphe or noeud_arrivee not in self.graphe:
            return False

        # Pour un graphe non orienté, vérifier les directions contradictoires
        if not self.est_oriente:
            # Vérifier si une arête existe déjà dans l'autre sens
            if noeud_arrivee in self.graphe[noeud_depart] or noeud_depart in self.graphe[noeud_arrivee]:
                return False

        # Ajouter l'arête
        self.graphe[noeud_depart][noeud_arrivee] = poids

        # Si le graphe est non orienté, ajouter l'arête dans l'autre sens
        if not self.est_oriente:
            self.graphe[noeud_arrivee][noeud_depart] = poids

        return True

    def ajouter_aretes(self, liste_aretes):
        aretes_ajoutees = []
        for noeud_depart, noeud_arrivee, poids in liste_aretes:
            if self.ajouter_arete(noeud_depart, noeud_arrivee, poids):
                aretes_ajoutees.append((noeud_depart, noeud_arrivee, poids))
        return aretes_ajoutees

    def dijkstra(self, depart, arrivee):
        distances = {noeud: float('inf') for noeud in self.graphe}
        distances[depart] = 0
        predecesseurs = {noeud: None for noeud in self.graphe}
        file_priorite = [(0, depart)]

        while file_priorite:
            distance_actuelle, noeud_actuel = heapq.heappop(file_priorite)

            if noeud_actuel == arrivee:
                chemin = []
                while noeud_actuel:
                    chemin.append(noeud_actuel)
                    noeud_actuel = predecesseurs[noeud_actuel]
                return chemin[::-1], distance_actuelle

            if distance_actuelle > distances[noeud_actuel]:
                continue

            for voisin, poids in self.graphe[noeud_actuel].items():
                distance = distance_actuelle + poids

                if distance < distances[voisin]:
                    distances[voisin] = distance
                    predecesseurs[voisin] = noeud_actuel
                    heapq.heappush(file_priorite, (distance, voisin))

        return None, None

    def dessiner_graphe(self, chemin_plus_court=None):
        plt.figure(figsize=(10, 6))
        
        # Créer le graphe NetworkX en fonction du type de graphe
        G = nx.DiGraph() if self.est_oriente else nx.Graph()
        
        for noeud in self.graphe:
            G.add_node(noeud)
        
        for noeud_depart, aretes in self.graphe.items():
            for noeud_arrivee, poids in aretes.items():
                G.add_edge(noeud_depart, noeud_arrivee, weight=poids)
        
        positions = nx.spring_layout(G, seed=42)
        
        # Options de dessin différentes selon le type de graphe
        if self.est_oriente:
            nx.draw(G, positions, with_labels=True, node_color='lightblue', 
                    node_size=500, arrows=True)
        else:
            nx.draw(G, positions, with_labels=True, node_color='lightblue', 
                    node_size=500, arrows=False)
        
        etiquettes_aretes = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, positions, edge_labels=etiquettes_aretes)
        
        if chemin_plus_court:
            aretes_chemin = list(zip(chemin_plus_court, chemin_plus_court[1:]))
            nx.draw_networkx_edges(G, positions, edgelist=aretes_chemin, 
                                   edge_color='r', width=2)
        
        plt.title(f"{'Orienté' if self.est_oriente else 'Non Orienté'} Recherche de Chemin")
        plt.axis('off')
        return plt