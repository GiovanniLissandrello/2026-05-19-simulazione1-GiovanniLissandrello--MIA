import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genere = None
        self._artista = None

    def fillDDGenre(self):

        lista_generi = self._model.getAllGeneri()

        for genere in lista_generi:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(data = genere,
                                   key = genere,
                                   text = genere.Name,
                                   on_click=self.read_genere)
            )
    def read_genere(self,e):
        if e.control.data is None:
            self._genere = None
        else:
            self._genere = e.control.data
            self._model.genere = e.control.data

    def handleCreaGrafo(self,e):
        self._model.buildDiGraph(self._genere.GenreId)

        n, m = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()

        best_nodo, best = self._model.getBestAffluenza()
        if best_nodo is None:
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato! "
                    f"Il grafo è costituito di {n} nodi ed {m} archi, miglior artista: {best_nodo.Name} con affluenza {best}"))

        archi = self._model.getArchi()
        self._view.txt_result.controls.append(
            ft.Text(f"Classifica: "))

        lista = list(archi)
        lista.sort(key=lambda x: x[2]["weight"],reverse=True)

        i = 0
        for u, v, peso in lista:
            if i <= 5:
                self._view.txt_result.controls.append(
                    ft.Text(f"{u} -> {v} | Peso: {peso}"))
                i += 1

        self.fillDDArtist()
        self._view.update_page()

    def fillDDArtist(self):

        lista_artisti = self._model.getArtisti(self._genere.GenreId)

        for artista in lista_artisti:
            self._view._ddArtist.options.append(
                ft.dropdown.Option(data = artista,
                                   key = artista,
                                   text = artista.Name,
                                   on_click=self.read_artista)
            )

    def read_artista(self,e):
        if e.control.data is None:
            self._artista = None
        else:
            self._artista = e.control.data

    def handleCammino(self,e):
        best, best_nodo = self._model.getPathV2(self._artista)
        self._view.txt_result.controls.append(
            ft.Text(f"Miglior nodo {best_nodo}"))

        for b in best:
            self._view.txt_result.controls.append(
                ft.Text(b))

        self._view.update_page()