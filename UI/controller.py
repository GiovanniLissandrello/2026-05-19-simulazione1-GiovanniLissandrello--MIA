import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genere = None

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
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato! "
                    f"Il grafo è costituito di {n} nodi ed {m} archi"))

        self._view.update_page()

    def handleCammino(self,e):
        pass