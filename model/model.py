import copy
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.idMap = {}

    def buildGraph(self, durata):
        self.graph.clear()
        nodi = DAO.getNodi(durata)
        for i in nodi:
            self.graph.add_node(i)
            self.idMap[i.id] = i
        archi = DAO.getArchi()
        for a in archi:
            if a[0] in self.idMap and a[1] in self.idMap:
                self.graph.add_edge(self.idMap[a[0]],self.idMap[a[1]])

    def componenteConnessa(self, album):
        compConn = list(nx.node_connected_component(self.graph, album))
        somma = 0
        for i in compConn:
            somma += i.durata
        return compConn, somma

    def getCammino(self, album, soglia):
        self.solBest = []
        self.durataMax = 0
        parziale = [album]
        self.ricorsione(parziale, album, soglia)
        print(self.durataMax, len(self.solBest), self.solBest)
        return self.solBest, self.durataMax

    def ricorsione(self, parziale, n, soglia):
        vicini = list(self.graph.neighbors(n))
        viciniAmmissibili = self.getAmmissibili(parziale, vicini, soglia)
        if len(viciniAmmissibili) == 0:
            durata = self.calcolaDurata(parziale)
            if durata > self.durataMax and len(parziale) > len(self.solBest):
                self.durataMax = durata
                self.solBest = copy.deepcopy(parziale)
        else:
            for v in viciniAmmissibili:
                durataAttuale = self.calcolaDurata(parziale)
                if durataAttuale+v.durata<soglia:
                    parziale.append(v)
                    self.ricorsione(parziale, v, soglia)
                    parziale.pop()



    def getAmmissibili(self, parziale, vicini, soglia):
        durataAttuale = self.calcolaDurata(parziale)
        ammisibili = []
        for v in vicini:
            if v not in parziale and durataAttuale+v.durata<soglia:
                ammisibili.append(v)
        return ammisibili


    def calcolaDurata(self, parziale):
        somma = 0
        for p in parziale:
            somma+=p.durata
        return somma
    def graphDetails(self):
        return len(self.graph.nodes), len(self.graph.edges)