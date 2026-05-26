import networkx as nx
import copy
from database.DAO import DAO
from model.Arco import Arco


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._dict_popolarita = {}
        self._lista_idCustomer = DAO.getAllIdCustomer() #lista di tutti gli ID dei Customer

    def buildDiGraph(self, genereId):
        self._graph.clear()
        self._nodi = self.getArtisti(genereId)
        self._graph.add_nodes_from(self._nodi)

        self._lista_popol = DAO.getPopolarita(genereId)
        for artista in self._lista_popol:
            self._dict_popolarita[artista[0]] = artista[1]  # dizionario con idArtista --> popolarità

        dict_artisti = {}
        for n in self._nodi:
            dict_artisti[n.ArtistId] = n

        for id in  self._lista_idCustomer:
            collegamento_tupla = DAO.getCollegamenti(id, dict_artisti, genereId)
            for tupla in collegamento_tupla:

                a1 = tupla[0]
                a2 = tupla[1]

                if a1 is None or a2 is None or a1 == a2:
                    continue

                if self._graph.has_edge(a1,a2) or self._graph.has_edge(a2,a1):
                    continue

                pop1 = self._dict_popolarita.get(a1.ArtistId, 0)
                pop2 = self._dict_popolarita.get(a2.ArtistId, 0)
                somma = pop1 + pop2

                if int(self._dict_popolarita.get(a1.ArtistId)) > int(self._dict_popolarita.get(a2.ArtistId)):
                    self._graph.add_edge(a1, a2, weight=somma)
                    continue

                elif int(self._dict_popolarita.get(a1.ArtistId)) < int(self._dict_popolarita.get(a2.ArtistId)):
                    self._graph.add_edge(a2, a1, weight=somma)
                    continue

                else:
                    self._graph.add_edge(a1, a2, weight=somma)
                    self._graph.add_edge(a2, a1, weight=somma)

    def getAllGeneri(self):
        return DAO.getAllGeneri()

    def getArtisti(self, genereId):
        return DAO.getArtisti(genereId)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getBestAffluenza(self):
        nodi = self._nodi

        best = 0
        best_nodo = None

        for n in nodi:
            archi_uscenti = self._graph.out_edges(n)
            archi_entranti = self._graph.in_edges(n)

            peso_uscenti = 0
            peso_entranti = 0

            for u,v in archi_uscenti:
                peso_uscenti = peso_uscenti + self._graph[u][v]["weight"]

            for u,v in  archi_entranti:
                peso_entranti = peso_entranti + self._graph[u][v]["weight"]

            affluenza =  peso_uscenti - peso_entranti

            if best < affluenza:
                best = affluenza
                best_nodo = n

        return best_nodo, best

    def getArchi(self):
        return (self._graph.edges(data = True))


    def getPathV2(self, v0):
        self._bestPath = []
        self._bestObjVal = 0

        parziale = [v0]

        listaVicini = self.getVicini(parziale[-1])
        parziale.append(listaVicini[0][0]) #listaVicini è una lista di tuple.  tupla --> (vicino, peso) --> [0][0] accede al vicino
        self._ricorsioneV2(parziale)

        return self._bestPath, self._bestObjVal


    def _ricorsioneV2(self, parziale):
        # 1 condizione di ottimalità, verifico se la parziale è migliore del best
        if self._score(parziale) > self._bestObjVal:
            self._bestPath = copy.deepcopy(parziale)
            self._bestObjVal = self._score(parziale)

        listaVicini = self.getVicini(parziale[-1])

        for v in listaVicini:
            if v[0] not in parziale and self._graph[parziale[-2]][parziale[-1]]["weight"] > v[1]:   #v[0] recupera il vicino, v[1] il peso
                parziale.append(v[0])
                self._ricorsioneV2(parziale)
                parziale.pop()
                return

    def _score(self, parziale):
        score = 0
        for i in range(0, len(parziale)-1):
            score += self._graph[parziale[i]][parziale[i+1]]["weight"]

        return score

    def getVicini(self, source):
        vicini = self._graph.neighbors(source)
        viciniTuples = []
        for v in vicini:
            viciniTuples.append((v, self._graph[source][v]["weight"]))

        viciniTuples.sort(key=lambda x: x[1], reverse=True)

        return viciniTuples
