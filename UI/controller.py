import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._choiceLocation = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        provider = self._view._ddProvider.value
        if provider is None:
            self._view.create_alert("Seleziona un provider!")
            return

        soglia = self._view._txtInDistanza.value
        if soglia == "":
            self._view.create_alert("Inserire una soglia!")
            return

        try:
            soglia = float(soglia)
        except ValueError:
            self._view.create_alert("Inserire un valore numerico!")
            return

        self._model.buildGraph(provider, soglia)

        nNodes, nEdges = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato. Il grafo ha {nNodes} nodi e {nEdges} archi."))
        self.fillDDTarget()
        self._view.update_page()

    def handleAnalizzaGrafo(self, e):
        nNodes, nEdges = self._model.getGraphDetails()
        if nNodes == 0 and nEdges == 0:
            self._view.create_alert("Attenzione, grafo vuoto.")
            return

        lista = self._model.getNodesMostVicini()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Nodi con più vicini: "))
        for l in lista:
            self._view.txt_result.controls.append(ft.Text(f"{l[0]} -- {l[1]}"))
        self._view.update_page()


    def handlePercorso(self, e):
        substring = self._view._txtInStringa.value
        if substring == "":
            self._view.create_alert("Attenzione, stringa non inserita.")
            return
        if self._choiceLocation is None:
            self._view.create_alert("Scegliere un target!")
            return

        path, source = self._model.getCammino(self._choiceLocation, substring)
        if not path:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Non ho trovato un cammino fra {source} e {self._choiceLocation}"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Ho trovato un cammino fra {source} e {self._choiceLocation}"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.update_page()

    def fillDD(self):
        providers = self._model.getProviders()
        providersDD = map(lambda x: ft.dropdown.Option(x),
                          providers)
        self._view._ddProvider.options = providersDD

    def fillDDTarget(self):
        locations = self._model.getAllLocations()

        locationsDD = map(lambda x: ft.dropdown.Option(data=x, text=x.location,
                                                       on_click=self.readChoiceLocation), locations)
        self._view._ddTarget.options.extend(locationsDD)

    def readChoiceLocation(self, e):
        if e.control.data is None:
            self._choiceLocation = None
        else:
            self._choiceLocation = e.control.data


