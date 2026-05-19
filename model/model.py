import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()

    def buildDiGraph(self, genereId):
        nodi = self.getArtisti(genereId)
        self._graph.add_nodes_from(nodi)

        lista_idCustomer = DAO.getAllIdCustomer()
        dict_popolarita = {}
        lista_popol = DAO.getPopolarita()

        for artista in lista_popol:
            dict_popolarita[artista[0]] = artista[1]  #dizionario con idArtista --> popolarità

        for id in lista_idCustomer:
            lista_canzoni_acquistate = DAO.getCanzoniAcquistateCustomer(id)

            for track in lista_canzoni_acquistate:
                Artista_track = DAO.getArtista(track.AlbumId)
                Artista = Artista_track[0]

                for track2 in lista_canzoni_acquistate:
                    Artista_track2 = DAO.getArtista(track2.AlbumId)
                    Artista2 = Artista_track2[0]

                    if self._graph.has_edge(Artista,Artista2) == False:
                        self._graph.add_edge(Artista,Artista2, weight = (int(dict_popolarita.get(Artista.ArtistId))) + int(dict_popolarita.get(Artista2.ArtistId)))
                    #controllare se sono uguali
    def getAllGeneri(self):
        return DAO.getAllGeneri()

    def getArtisti(self, genereId):
        return DAO.getArtisti(genereId)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)