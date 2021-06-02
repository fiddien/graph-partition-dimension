#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 10:13:31 2021

@author: ilmaaliyaf
"""
import networkx as nx
from partition import partition


class Graph(nx.graph.Graph):
    def __init__(self, graph_type='', parameter=[]):
        if graph_type not in ['path', 'cycle', 'complete', 'complete_bipartite']:
            self.graph = nx.empty_graph()
            self.graph_params = None
        else:
            self.define_type(graph_type, parameter)

        self.basis = [{'p': '', 'r': ''}]
        self.pd = None
        self.count = 0

    def define_type(self, graph_type, parameter):
        self.graph_type = graph_type
        self.graph_params = parameter
        if graph_type not in ['path', 'cycle', 'complete', 'complete_bipartite']:
            raise ("Choose type between path, cycle, complete, and complete_bipartite")
        else:
            self.graph = eval('nx.' + graph_type + '_graph(*parameter)')

    def diam(self):
        return nx.diameter(self.graph)

    def distance(self):
        return dict(nx.all_pairs_shortest_path_length(self.graph))

    def find_pd(self,
                num_basis=1,
                lower_bound=2,
                upper_bound='',
                print_result=False):
        """ find basis for this graph """
        V = list(self.graph)
        basis_ = []
        if type(upper_bound) != int:
            upper_bound = self.graph.order() + 1

        i = 0
        for k in range(lower_bound, upper_bound):
            partitions = partition(V, k)
            for j, P in enumerate(partitions):
                if j < self.count:
                    continue
                resolving, representation = self.is_resolving(P)
                if resolving:  # add P into basis_dict
                    basis_.append({'p': P, 'r': representation})
                    self.basis = basis_
                    self.pd = len(basis_[-1]['p'])
                    i += 1
                    if print_result:
                        print(P)
                    if i + 1 > num_basis:
                        self.count = j
                        return

    def is_resolving(self, partition):
        r = {}
        d = self.distance()
        for v in self.graph.nodes:
            r[v] = []
            for P in partition:
                dvP = d[v][min(P, key=d[v].get)]
                r[v].append(dvP)
        r_reversed = {str(val): key for key, val in r.items()}
        return len(r) == len(r_reversed), r

    def r(self, partition):
        r = {}
        d = self.distance()
        for v in self.graph.nodes:
            r[v] = []
            for P in partition:
                dvP = d[v][min(P, key=d[v].get)]
                r[v].append(dvP)
        return r

class productGraph(Graph):

    def __init__(self, G, H, product_type, product_params):
        self.component_graphs = (G, H)
        self.product_type = product_type
        self.product_params = product_params
        self.graph_type = 'product'

        if product_type == 'k-strong':
            self.k_strong()
        elif product_type == 'cartesian':
            self.cartesian()
        else:
            self.graph = nx.empty_graph()

        self.count = None
        self.basis = [{'p': '', 'r': ''}]
        self.pd = None

    def k_strong(self):
        G = self.component_graphs[0]
        H = self.component_graphs[1]
        if self.product_params == 1:
            self.graph = nx.strong_product(G.graph, H.graph)
        else:
            P = nx.cartesian_product(G.graph, H.graph)
            dG = G.distance()
            dH = H.distance()
            jumping_vertex = []
            for u in P.nodes:
                for v in P.nodes:
                    if dG[u[0]][v[0]] == self.product_params \
                            and dH[u[1]][v[1]] == self.product_params:
                        P.add_edge(u, v)
                        if v not in jumping_vertex:
                            jumping_vertex.append(v)
            self.graph = P
            self.jumping_vertex = jumping_vertex

    def cartesian(self):
        G = self.component_graphs[0]
        H = self.component_graphs[1]
        self.graph = nx.cartesian_product(G.graph, H.graph)