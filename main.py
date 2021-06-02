import sys
import PyQt5.QtWidgets as Widget
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
import networkx as nx
from graph_object import Graph, productGraph
from pyvis.network import Network

class MainProgram(Widget.QComboBox):

    def __init__(self):
        super(MainProgram, self).__init__()

        self.initials = ('g', 'h', 'p')
       
        self.graph_type = ['Path', 'Cycle', 'Complete', 'Complete Bipartite']
                       # 'Wheel', 'Wheel (m-step)', 'Jahangir Generalised',
                       # 'Lollipop']

        self.product_type = ['Cartesian', 'k-strong']
        
        self.initial_graph_param = {'path': 2, 'cycle': 3, 'complete': 2,
                                    'complete_bipartite': 1, 'k-strong':1,
                                    '': 1, 'cartesian': 1}
        
        # === LEFT SECTION INITIALISATION: SLIDERS ===
        def init_slider_widget():
            slider = Widget.QSlider(Qt.Horizontal)
            slider.setValue(1)
            slider.setFocusPolicy(Qt.StrongFocus)
            slider.setTickPosition(Widget.QSlider.TicksBothSides)
            slider.setTickInterval(1)
            slider.setSingleStep(1)
            slider.setMinimum(1)
            slider.setMaximum(10)
            slider.setSingleStep(1)
            return slider

        self.slider = {}
        self.view = {}
        for x in self.initials:
            self.slider[x] = (init_slider_widget(), init_slider_widget())
            self.view[x] = QWebEngineView()
        
        # === GRAPH OBJECTS INITIALISATION ===
        self.select_graph = {}
        for x in self.initials[:2]:
            self.select_graph[x] = Widget.QComboBox(self)
            self.select_graph[x].addItems(self.graph_type)
            self.select_graph[x].setCurrentIndex(-1)
        
        self.select_graph['p'] = Widget.QComboBox(self)
        self.select_graph['p'].addItems(self.product_type)
        self.select_graph['p'].setCurrentIndex(-1)
        
        # === BASIS BUTTON INITIALISATION ===
        self.basisButtonBox = Widget.QGroupBox()

        self.result_button = {}
        for i, x in enumerate(self.initials):
            self.result_button[x] = Widget.QPushButton()
            self.result_button[x].setText(f'Search Basis of {x.upper()}')
            self.result_button[x].clicked.connect(self.basis_updater)
            self.result_button[x].setEnabled(False)

        # === RESULT BOX INITIALISATION ===
        self.viewBox = Widget.QGroupBox()
        self.resultBox = Widget.QGroupBox()
        
        self.result = {}
        for x in self.initials:
            self.result[x] = Widget.QLabel(
                f'Basis of {x.upper()}:\nNone\nRepresentations of V({x.upper()}):\nNone', self) 

        gr = Graph('path', [1])
        # === GRAPH-RELATED VARIABLES INITIALISATION ===
        self.w = '409px'
        self.h = '420px'
        self.nt = {x: {'type': '', 'params': '', 'pd': 100,
                       'nt': Network(height=self.h, width=self.w),
                       'nx': gr} 
                   for x in self.initials}

        # CALLING UI
        self.unit_ui()

        self.show()
        self.setWindowState(Qt.WindowMaximized)
        
    def center(self):
        qr = self.frameGeometry()
        cp = Widget.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def unit_ui(self):
        self.setGeometry(100, 100, 1200, 600)
        self.center()
        self.setWindowTitle('Partition Dimension of Graphs')
        grid = Widget.QGridLayout()
        grid.setColumnStretch(1, 6)
        grid.setRowStretch(1, 2)
        self.setLayout(grid)

        # ADD SELECT GRAPH & RESULT SECTION
        self.box_result()
        result_layout = Widget.QHBoxLayout()
        result_layout.addWidget(self.resultBox)
        grid.addLayout(result_layout, 2, 0, 1, 3)
        
        # ADD GRAPH VIEWER
        self.viewer()
        view_layout = Widget.QHBoxLayout()
        view_layout.addWidget(self.viewBox)
        grid.addLayout(view_layout, 1, 1),

    def viewer(self):
        layout = Widget.QGridLayout()
        
        for i, x in enumerate(self.initials):
            self.nt[x]['nt'].from_nx(self.nt[x]['nx'].graph)
            self.nt[x]['nt'].save_graph(f'view_graph_{x}.html')
            with open(f'view_graph_{x}.html', 'r') as f:
                html = f.read()
            self.view[x].setHtml(html)
            layout.addWidget(self.view[x], 0, i, alignment=Qt.AlignCenter)
        
        layout.setSpacing(10)
        self.viewBox.setLayout(layout) 

    def box_result(self):
        layout = Widget.QGridLayout()
        layout.setSpacing(10)

        label = {}
        label['g'] = Widget.QLabel('Select G', self)
        label['h'] = Widget.QLabel('Select H', self)
        label['p'] = Widget.QLabel('Select Product', self)

        for i, x in enumerate(self.initials):
            layout.addWidget(label[x], 0, i*2)
            layout.addWidget(self.select_graph[x], 1, i*2)
            layout.addWidget(self.result_button[x], 4, i*2)

            scroll = Widget.QScrollArea()
            scroll.setWidget(self.result[x])
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(150)
            scroll.setViewportMargins(5, 5, 5, 5)
            layout.addWidget(scroll, 0, i*2+1, 5, 1)

            # manage signal
            self.select_graph[x].activated.connect(self.update_graph)
            self.select_graph[x].activated[str].connect(self.on_product)
            self.select_graph[x].currentIndexChanged['QString'].connect(self.disable_widget)

            # GRAPH SLIDERS
            for j in range(2):
                # add to layout
                layout.addWidget(self.slider[x][j], j+2, i*2)

                # manage signal
                self.slider[x][j].valueChanged.connect(self.update_graph)
                self.slider[x][j].valueChanged[int].connect(self.on_product)
        
        self.select_graph['p'].setEnabled(False)
        self.slider['p'][0].setEnabled(False)
        self.slider['p'][1].setEnabled(False)

        notice = Widget.QLabel('Copyright © 2021 by Ilma Aliya Fiddien - All rights reserved', self)
        layout.addWidget(notice, 5, 0, 6, 0, Qt.AlignCenter)

        self.resultBox.setLayout(layout)
        
    def disable_widget(self, currentIndex):
        # if both g and h are active, then make p active
        if self.select_graph['h'].isEnabled() and self.select_graph['h'].isEnabled():
            self.select_graph['p'].setEnabled(True)
        else:
            self.select_graph['p'].setEnabled(False)

        # if p is active then make its sliders and button active
        if self.select_graph['p'].isEnabled() == False:
            self.slider['p'][0].setEnabled(False)
            self.slider['p'][1].setEnabled(False)
            self.result_button['p'].setEnabled(False)

        sender = self.sender()
        # if g or h are in those list, make the 2nd slider (parameter) active
        if currentIndex in ['Lollipop', 'Complete Bipartite', 'Wheel (m-step)',
                            'Jahangir Generalised']:
            if sender is self.select_graph['g']:
                self.slider['g'][1].setEnabled(True)
            if sender is self.select_graph['h']:
                self.slider['h'][1].setEnabled(True)
        else:
            if sender is self.select_graph['g']:
                self.slider['g'][1].setEnabled(False)
            if sender is self.select_graph['h']:
                self.slider['h'][1].setEnabled(False)

        if currentIndex in ['k-strong']:
            self.slider['p'][0].setEnabled(True)
        elif currentIndex in ['cartesian']:
            self.slider['p'][0].setEnabled(False)
            self.slider['p'][1].setEnabled(False)
        else:
            self.slider['p'][0].setEnabled(False)
     
    # =============================
    # DRAWING ON THE CANVAS
    # =============================

    def graph_drawer(self, graph, title, x):
        """ Function to draw the updated graph into it's canvas """
        
        graph = nx.relabel_nodes(graph, lambda node: str(node))
        nt = Network(height=self.h, width=self.w)
        nt.from_nx(graph)

        if x == 'p':
            layout = {}
            for v in graph.nodes:
                v_ = eval(v)
                layout[v] = ([v_[0], v_[1]])
            for node in nt.nodes:
                node["x"] = layout[node['id']][0] * 100
                node["y"] = layout[node['id']][1] * 100

            nt.toggle_physics(False)

        nt.save_graph(f'view_graph_{x}.html')
        with open(f'view_graph_{x}.html', 'r') as f:
            html = f.read()
            self.view[x].setHtml(html)

        self.nt[x]['nt'] = nt
        
    def update_graph(self):
        """ Function to set graph G """
        s = self.sender()
        if s in [self.select_graph['g'], self.slider['g'][0], self.slider['g'][1]]:
            x = 'g'
        elif s in [self.select_graph['h'], self.slider['h'][0], self.slider['h'][1]]:
            x = 'h'
        else:
            x = 'p'

        graph_type = '_'.join(str(self.select_graph[x].currentText()).lower().split())
        m = self.slider[x][0].value()

        if m < self.initial_graph_param[graph_type]:
            m = self.initial_graph_param[graph_type]
            self.slider[x][0].setValue(self.initial_graph_param[graph_type])
        
        if self.slider[x][1].isEnabled():
            n = self.slider[x][1].value()
            graph = Graph(graph_type, [m, n])
            graph_params = [m, n]
        else:
            graph = Graph(graph_type, [m])
            graph_params = [m]

        self.nt[x]['nx'] = graph
        self.graph_drawer(graph.graph, f'{graph_type} {graph_params}', x)

        # enabling basis updater button
        self.result_button[x].setEnabled(True)
        self.result[x].setText(f'Basis of {x.upper()}:\nNone\nRepresentations of V({x.upper()}):\nNone')
        self.change = True

    def on_product(self):
        """ Function to set graph product P """
        
        product_type = '_'.join(str(self.select_graph['p'].currentText()).lower().split())
        
        p = productGraph(self.nt['g']['nx'], self.nt['h']['nx'], 
                              product_type, self.slider['p'][0].value())
        
        self.nt['p']['nx'] = p
        self.graph_drawer(p.graph, p.product_type + " " + str(p.product_params), 'p')

        # enabling basis updater button
        self.result_button['p'].setEnabled(True)
        self.change = True
        
    # ======================
    # DEALING WITH THE BASIS
    # ======================
                
    def basis_updater(self):
        """ Function to update basis of the updated graph """
        
        # 1 search partition dimension and it's basis
        s = self.sender()
        if s == self.result_button['g']:
            x = 'g'
        elif s == self.result_button['h']:
            x = 'h'
        else:
            x = 'p'

        # prepare to continue checking the partitions from last iteration
        # because we are dealing with the same graph
        if self.change == False:
            count = self.nt[x]['nx'].count
            num_basis = 2
            pd = self.nt[x]['pd']
        else:
            count = 0
            num_basis = 1
            pd = self.nt[x]['nx'].graph.order()
            
        graph = self.nt[x]['nx']
        graph.count = count # continue from the last checked partition
        graph.find_pd(num_basis=num_basis) # search for partition dimension
        basis = graph.basis[-1]['p']
        r = graph.basis[-1]['r']
        
        for v in graph.graph.nodes:
            graph.graph.nodes[v]['title'] = str(r[v])
            graph.graph.nodes[v]['group'] = r[v].index(0) + 1
        
        self.graph_drawer(graph.graph, graph.graph_type, x)
        
        # 2 form the text to show
        G = x.upper()

        if pd < graph.pd:
            part_type = 'Resolving partition'
            connection = '<='
        else:
            part_type = 'Basis'
            connection = '='

        b_text = part_type + ' of ' + G + ':\n' \
                + str(basis) \
                + '\n\npd(' + G + ') '+ connection + ' ' + str(graph.pd)
        
        rep = ''
        for v in r.keys():
            rep = rep + 'r(v_' + str(v) + ' | B' + G + ') = ' \
                  + str(tuple(r[v])) + '\n'
                  
        b_text = b_text + '\n\nRepresentations of V(' + G \
                        + '):\n' + rep
        
        # 3 send signal to result box
        self.result[x].setText(b_text)

        self.change = False

if __name__ == '__main__':
    app = Widget.QApplication(sys.argv)
    # app.aboutToQuit.connect(app.deleteLater)
    app.setStyle("Fusion")
    screen = MainProgram()
    result = app.exec_()
    del screen
    del app
    sys.exit(result)
