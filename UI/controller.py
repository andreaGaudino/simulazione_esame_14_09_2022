import warnings

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.album = None



    def handleCreaGrafo(self, e):
        durata = self._view.txtDurata.value
        if durata == "":
            self._view.create_alert("Durata non inserita")
            self._view.update_page()
            return
        try:
            intDurata = int(durata)
        except ValueError:
            self._view.create_alert("Durata inserita non numerica")
            self._view.update_page()
            return
        self._model.buildGraph(intDurata)
        n, e = self._model.graphDetails()
        self._view.txtGrafo.clean()
        self._view.txtGrafo.controls.append(ft.Text(f"Grafo creato con {n} nodi e {e} archi"))
        self.fillDD(list(self._model.graph.nodes))
        self._view.update_page()

    def handleCompConnessa(self, e):
        if self.album is None:
            self._view.create_alert("Album non selezionato")
            self._view.update_page()
            return
        compConn, durata = self._model.componenteConnessa(self.album)
        self._view.txtCompConn.clean()
        self._view.txtCompConn.controls.append(ft.Text(f"Componente connessa di {self.album} di lunghezza {len(compConn)}\nCon durata complessiva {durata}"))
        self._view.update_page()

    def handleSimulazione(self, e):
        if self.album is None:
            self._view.create_alert("Album non selezionato")
            self._view.update_page()
            return
        durataMax = self._view.soglia.value
        if durataMax == "":
            self._view.create_alert("Durata massima non inserita")
            self._view.update_page()
            return

        try:
            durataInt = int(durataMax)
        except ValueError:
            self._view.create_alert("Durata massima inserita non numerica")
            self._view.update_page()
            return

        solBest, durata = self._model.getCammino(self.album, durataInt)
        self._view.txtSimulazione.clean()
        self._view.txtSimulazione.controls.append(ft.Text(f"Durata massima {durata}"))
        for n in solBest:
            self._view.txtSimulazione.controls.append(ft.Text(f"{n}"))
        self._view.update_page()


    def fillDD(self, nodi):
        nodiDD = list(map(lambda x:ft.dropdown.Option(text=x.title, key=x, on_click=self.getNodo), nodi))
        self._view.ddAlbum.options = nodiDD
        self._view.update_page()

    def getNodo(self,e):
        if e.control.key is None:
            pass
        else:
            self.album = e.control.key




           