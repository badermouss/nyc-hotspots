import copy
import random

import networkx as nx
from geopy.distance import distance
from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodes = None
        self._graph = nx.Graph()
        self._providers = DAO.getAllProviders()
        self._bestPath = []
        self._bestLen = 0

    def buildGraph(self, provider, soglia):
        self._graph.clear()
        self._nodes = DAO.getLocationsOfProviderV2(provider)
        self._graph.add_nodes_from(self._nodes)
        for u in self._nodes:
            for v in self._nodes:
                if u != v:
                    dist = distance((u.latitude, u.longitude), (v.latitude, v.longitude)).km
                    if dist < soglia:
                        if not self._graph.has_edge(u, v):
                            self._graph.add_edge(u, v, weight=dist)
        print(f"N nodes: {len(self._graph.nodes)} -- N edges: {len(self._graph.edges)}")

    def getNodesMostVicini(self):
        listTuples = []
        for v in self._nodes:
            listTuples.append((v, len(list(self._graph.neighbors(v)))))
        listTuples.sort(key=lambda x: x[1], reverse=True)
        # result = filter(lambda x: x[1] == listTuples[0][1], listTuples)

        result2 = [x for x in listTuples if x[1] == listTuples[0][1]]
        return result2

    def getCammino(self, target, substring):
        sources = self.getNodesMostVicini()
        source = sources[random.randint(0, len(sources)-1)][0]
        if not nx.has_path(self._graph, source, target):
            print(f"{source} e {target} non sono connessi.")
            return [], source

        self._bestPath = []
        self._bestLen = 0
        parziale = [source]
        self._ricorsione(parziale, target, substring)

        return self._bestPath, source

    def _ricorsione(self, parziale, target, substring):
        if parziale[-1] == target:
            if len(parziale) > self._bestLen:
                self._bestPath = copy.deepcopy(parziale)
                self._bestLen = len(parziale)
            return
        for v in self._graph.neighbors(parziale[-1]):
            if v not in parziale and substring not in v.location:
                parziale.append(v)
                self._ricorsione(parziale, target, substring)
                parziale.pop()

    def getProviders(self):
        return self._providers

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllLocations(self):
        return self._graph.nodes
