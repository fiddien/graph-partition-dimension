import sys
import PyQt5
import PyQt5.QtWidgets as Widget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx


class MainProgram(Widget.QComboBox):

    def __init__(self):
        super(MainProgram, self).__init__()
        QFont().setPointSize(20)

        # LEFT SECTION INITIALISATION
        self.slider_gm = Widget.QSlider(Qt.Horizontal)
        self.slider_gn = Widget.QSlider(Qt.Horizontal)
        self.slider_hm = Widget.QSlider(Qt.Horizontal)
        self.slider_hn = Widget.QSlider(Qt.Horizontal)
        self.slider_p = Widget.QSlider(Qt.Horizontal)
        self.slider_gm.setValue(1)
        self.slider_gn.setValue(1)
        self.slider_hm.setValue(1)
        self.slider_hn.setValue(1)
        self.slider_p.setValue(1)

        self.graphs = ['Path','Cycle','Star','Complete','Complete Bipartite']#,
                       # 'Wheel', 'Wheel (m-step)', 'Jahangir Generalised',
                       # 'Lollipop']
        self.products = {'Cartesian': ('nx.cartesian_product', u'$\u2610$'),
                         'N-Strong' : ('nx.cartesian_product', r'$\boxtimes_N$'),
                         # 'Rooted'   : ('nx.rooted_product', r'$\circ$'),
                         'Tensor'   : ('nx.tensor_product', r'$\times$'),
                         'Lexicographic': ('nx.lexicographic_product', r'$\cdot$'),
                         '==No product==': ''}

        self.graph_g = Widget.QComboBox(self)
        self.graph_g.addItems(self.graphs)
        self.graph_h = Widget.QComboBox(self)
        self.graph_h.addItems(self.graphs)
        self.product = Widget.QComboBox(self)
        self.product.addItems(self.products.keys())
        self.basisButtonBox = Widget.QGroupBox()

        self.graph_g.setCurrentIndex(-1)
        self.graph_h.setCurrentIndex(-1)
        self.product.setCurrentIndex(-1)

        # FIGURE CANVAS INITIALISATION
        self.fig = plt.figure()
        self.fig.set_tight_layout(True)
        self.ax_g = plt.subplot(131)
        self.ax_h = plt.subplot(132)
        self.ax_p = plt.subplot(133)
        self.ax_g.axis('off')
        self.ax_h.axis('off')
        self.ax_p.axis('off')
        self.canvas = FigureCanvas(self.fig)

        # RESULT BOX INITIALISATION
        self.resultBox = Widget.QGroupBox()
        self.header_bg = Widget.QLabel('Basis of G:\nNone\nRepresentations of V(G):\nNone', self)
        self.header_bh = Widget.QLabel('Basis of H:\nNone\nRepresentations of V(H):\nNone', self)
        self.header_bp = Widget.QLabel('Basis of P:\nNone\nRepresentations of V(P):\nNone', self)


        # GRAPH-RELATED VARIABLES INITIALISATION
        self.g = nx.empty_graph(1)
        self.h = nx.empty_graph(1)
        self.p = nx.empty_graph(1)
        self.title_g = ''
        self.title_h = ''
        self.title_p = ''
        self.colors = ('b','r','g','yellow','c','m','orange','lime','silver',
                       'pink','coral','teal','royalblue','slategray','darkkhaki',
                       'maroon', 'purple','lightblue','olive','gold')
        self.pd_g = 2 # set default as lower bound
        self.pd_h = 2 # set default as lower bound
        self.pd_p = 2 # set default as lower bound
        self.basis_g = [[0]]
        self.basis_h = [[0]]
        self.basis_p = [[0]]
        self.reverse = False

        self.unit_ui()

    def unit_ui(self):

        self.setGeometry(100, 100, 1200, 600)
        self.center()
        self.setWindowTitle('Partition Dimension of Graph')
        grid = Widget.QGridLayout()
        grid.setColumnStretch(1,2)
        self.setLayout(grid)

        # ADD CHOOSING GRAPH SECTION
        self.box_select_graph() # call the func defining this
        select_graph_layout = Widget.QVBoxLayout()
        select_graph_layout.addWidget(self.selectGraphBox,alignment=Qt.AlignTop)
        grid.addLayout(select_graph_layout, 1, 0)

        # ADD GRAPH BASIS UPDATE BUTTONS
        self.box_basis_button() # call the func defining this
        update_basis_layout = Widget.QVBoxLayout()
        update_basis_layout.addWidget(self.basisButtonBox)
        grid.addLayout(update_basis_layout, 2, 0)

        # ADD FIGURE CANVAS
        grid.addWidget(self.canvas, 1, 1)

        # ADD RESULT BOX
        self.box_result()
        result_layout = Widget.QHBoxLayout()
        result_layout.addWidget(self.resultBox)
        grid.addLayout(result_layout, 2, 1)

        self.show()

    def box_select_graph(self):

        # GRAPH G BUTTON & SLIDERS
        graph_g_lbl = Widget.QLabel('Select G', self)
        self.slider_gm.setFocusPolicy(Qt.StrongFocus)
        self.slider_gm.setTickPosition(Widget.QSlider.TicksBothSides)
        self.slider_gm.setTickInterval(1)
        self.slider_gm.setSingleStep(1)
        self.slider_gm.setMinimum(1)
        self.slider_gm.setMaximum(10)
        self.slider_gm.setSingleStep(1)
        self.slider_gn.setFocusPolicy(Qt.StrongFocus)
        self.slider_gn.setTickPosition(Widget.QSlider.TicksBothSides)
        self.slider_gn.setTickInterval(1)
        self.slider_gn.setSingleStep(1)
        self.slider_gn.setMinimum(1)
        self.slider_gn.setMaximum(10)
        self.slider_gn.setSingleStep(1)

        # GRAPH H BUTTON & SLIDERS
        graph_h_lbl = Widget.QLabel('Select H', self)
        self.slider_hm.setFocusPolicy(PyQt5.QtCore.Qt.StrongFocus)
        self.slider_hm.setTickPosition(Widget.QSlider.TicksBothSides)
        self.slider_hm.setTickInterval(1)
        self.slider_hm.setSingleStep(1)
        self.slider_hm.setMinimum(1)
        self.slider_hm.setMaximum(10)
        self.slider_hm.setSingleStep(1)
        self.slider_hn.setFocusPolicy(PyQt5.QtCore.Qt.StrongFocus)
        self.slider_hn.setTickPosition(Widget.QSlider.TicksBothSides)
        self.slider_hn.setTickInterval(1)
        self.slider_hn.setSingleStep(1)
        self.slider_hn.setMinimum(1)
        self.slider_hn.setMaximum(10)
        self.slider_hn.setSingleStep(1)

        # OPERATION PRODUCT BUTTON
        product_lbl = Widget.QLabel('Select Product', self)
        self.slider_p.setFocusPolicy(PyQt5.QtCore.Qt.StrongFocus)
        self.slider_p.setTickPosition(Widget.QSlider.TicksBothSides)
        self.slider_p.setTickInterval(1)
        self.slider_p.setSingleStep(1)
        self.slider_p.setMinimum(1)
        self.slider_p.setMaximum(10)
        self.slider_p.setSingleStep(1)

        # SELECTING ACTIVITY
        # on graph g
        self.graph_g.activated.connect(self.on_graph_g)
        self.graph_g.currentIndexChanged['QString'].connect(self.disableWidget)
        self.slider_gn.valueChanged.connect(self.on_graph_g)
        self.slider_gm.valueChanged.connect(self.on_graph_g)
        # on product operation
        self.product.activated[str].connect(self.on_product)
        self.product.currentIndexChanged['QString'].connect(self.disableWidget)
        self.slider_p.valueChanged[int].connect(self.on_product)
        # on graph h
        self.graph_h.activated[str].connect(self.on_graph_h)
        self.graph_h.currentIndexChanged['QString'].connect(self.disableWidget)
        self.slider_hn.valueChanged[int].connect(self.on_graph_h)
        self.slider_hm.valueChanged[int].connect(self.on_graph_h)

        # UPDATE PRODUCT GRAPH
        # if sliders on graph g are changed
        self.graph_g.activated[str].connect(self.on_product)
        self.slider_gn.valueChanged[int].connect(self.on_product)
        self.slider_gm.valueChanged[int].connect(self.on_product)
        # if sliders on graph h are changed
        self.graph_h.activated[str].connect(self.on_product)
        self.slider_hn.valueChanged[int].connect(self.on_product)
        self.slider_hm.valueChanged[int].connect(self.on_product)

        self.slider_p.valueChanged[int].connect(self.on_product)

        # LAYOUTING
        self.selectGraphBox = Widget.QGroupBox()
        layout = Widget.QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(graph_g_lbl)
        layout.addWidget(self.graph_g)
        layout.addWidget(self.slider_gm)
        layout.addWidget(self.slider_gn)
        layout.addWidget(product_lbl)
        layout.addWidget(self.product)
        layout.addWidget(self.slider_p)
        layout.addWidget(graph_h_lbl)
        layout.addWidget(self.graph_h)
        layout.addWidget(self.slider_hm)
        layout.addWidget(self.slider_hn)

        self.selectGraphBox.setLayout(layout)

    def box_basis_button(self):
        self.basisButtonBox = Widget.QGroupBox()
        self.button_bg = Widget.QPushButton()
        self.button_bh = Widget.QPushButton()
        self.button_bp = Widget.QPushButton()

        self.button_bg.setText('Search Basis of G')
        self.button_bh.setText('Search Basis of H')
        self.button_bp.setText('Search Basis of P')

        self.button_bg.clicked.connect(lambda:self.graph_basis_updater(self.button_bg))
        self.button_bh.clicked.connect(lambda:self.graph_basis_updater(self.button_bh))
        self.button_bp.clicked.connect(lambda:self.graph_basis_updater(self.button_bp))

        layout = Widget.QVBoxLayout()
        layout.addWidget(self.button_bg, alignment=Qt.AlignCenter)
        layout.addWidget(self.button_bh, alignment=Qt.AlignCenter)
        layout.addWidget(self.button_bp, alignment=Qt.AlignCenter)

        self.button_bg.setEnabled(False)
        self.button_bh.setEnabled(False)
        self.button_bp.setEnabled(False)
        self.basisButtonBox.setLayout(layout)

    def box_result(self):
        layout = Widget.QHBoxLayout()

        scroll_g = Widget.QScrollArea()
        scroll_g.setWidget(self.header_bg)
        scroll_g.setWidgetResizable(True)
        scroll_g.setFixedHeight(200)
        scroll_h = Widget.QScrollArea()
        scroll_h.setWidget(self.header_bh)
        scroll_h.setWidgetResizable(True)
        scroll_h.setFixedHeight(200)
        scroll_p = Widget.QScrollArea()
        scroll_p.setWidget(self.header_bp)
        scroll_p.setWidgetResizable(True)
        scroll_p.setFixedHeight(200)

        layout.addWidget(scroll_g)
        layout.addWidget(scroll_h)
        layout.addWidget(scroll_p)
        layout.setSpacing(10)
        self.resultBox.setLayout(layout)

    def graph_generator(self, graph_type, m, n, a):
        g = nx.empty_graph(m)
        title = ''
        self.reverse = False
        pd = 2
        basis = [[0]]

        if graph_type == 'Path':
            if m < 2:
                m = 2
                eval('self.slider_' + a + 'm.setValue(2)')
            title = r'$\ P_{' + str(m) + '}$'
            g = nx.path_graph(m)
            # setting the partition dimension and basis
            pd = 2
            basis.append([x for x in range(1,m)])

        elif graph_type == 'Cycle':
            if m < 3:
                m = 3
                eval('self.slider_' + a + 'm.setValue(3)')
            g = nx.cycle_graph(m)
            title = r'$\ C_{' + str(m) + '}$'
            # setting the partition dimension and basis
            pd = 3
            basis.append([1])
            basis.append([x for x in range(2,m)])

        elif graph_type == 'Complete':
            if m < 2:
                m = 1
                eval('self.slider_' + a + 'm.setValue(1)')
            g = nx.complete_graph(m)
            title = r'$\ K_{' + str(m) + '}$'
            # setting the partition dimension and basis
            pd = m
            for x in range(1,m):
                basis.append([x])

        elif graph_type == 'Star':
            if m < 3:
                m = 3
                eval('self.slider_' + a + 'm.setValue(3)')
            g = nx.star_graph(m)
            title = r'$\ S_{' + str(m) + '}$'
            # setting the partition dimension and basis
            pd = m
            basis[0].append(1)
            for x in range(2,m+1):
                basis.append([x])

        # elif graph_type == 'Wheel':
        #     if m < 3:
        #         m = 3
        #         eval('self.slider_' + a + 'm.setValue(3)')
        #     g = nx.wheel_graph(m+1)
        #     title = r'$\ W_{' + str(m) + '}$'
        #     # setting the partition dimension and basis
        #     if m == 3:
        #         pd = 4
        #         for i in range(3):
        #             basis.append([i+1])
        #     elif 4 <= m <= 7:
        #         pd = 3
        #         k = int(m/2) + 1
        #         for x in range(1,k):
        #             basis[0].append(x)
        #         basis.append([x for x in range(k,k+int((m-k)/2+1))])
        #         basis.append([x for x in range(k+int((m-k)/2+1),m+1)])
        #     '''elif 8 <= m <= 19:
        #         pd = 4
        #         k = int(m/3) + 1
        #         for x in range(1,k):
        #             basis[0].append(x)
        #         k_ = k + int((m-k)/3) + 1
        #         basis.append([x for x in range(k,k_)])
        #         k__ = k_ + int((m-k_)/3) + 1
        #         basis.append([x for x in range(k_,k__)])
        #         basis.append([x for x in range(k__,m+1)])'''
        #
        # elif graph_type == 'Wheel (m-step)':
        #     if m < 3:
        #         m = 3
        #         eval('self.slider_' + a + 'm.setValue(3)')
        #     g = nx.wheel_graph(m+1)
        #     k = m
        #     for c in range(n-1):
        #         vc = []
        #         for i in range(1,m+1):
        #             g.add_node(k+i)
        #             g.add_edge(0,k+i)
        #             vc.append(k+i)
        #         for i in range(1,m+1):
        #             g.add_edge(k+i,vc[i-2])
        #         k += m
        #     title = r'$\ W_{' + str(m) + ',' + str(n) + '}$'
        #     # setting the partition dimension and basis
        #     pd = 2 * int((m*n)**(1/2)+1) + 1
        #     self.reverse = True

        elif graph_type == 'Complete Bipartite' and m >= 2:
            g = nx.complete_bipartite_graph(m,n)
            title = r'$\ K_{' + str(m) + ',' + str(n) + '}$'
            # setting the partition dimension and basis
            # pd =

        elif graph_type == 'Lollipop' and m >= 2:
            g = nx.lollipop_graph(m,n)
            title = r'$\ K_{' + str(m) + ',' + str(n) + '}$'
            # setting the partition dimension and basis
            if m >= 3: pd = m
            for i in range(1,m-2):
                basis.append([i])
            basis.append([x for x in range(m-2,m+n-1)])
            basis.append([m+n-1])

        # elif graph_type == 'Jahangir Generalised':
        #     if n < 3:
        #         n = 3
        #         eval('self.slider_' + a + 'n.setValue(3)')
        #     g = nx.cycle_graph(m*n)
        #     g.add_node(m*n)
        #     v = 0
        #     for i in range(n):
        #         g.add_edge(m*n, v)
        #         v += m
        #     title = r'$\ J_{' + str(m) + ',' + str(n) + '}$'
        #     # setting the partition dimension and basis
        #     if 3 <= n <= 5:
        #         pd = 3
        #         if n == 3:
        #             s1 = [x for x in range(0,m*n+1,m)]
        #             for x in range(m*(n-1),m*n):
        #                 if x not in s1: s1.append(x)
        #             if m == 3:
        #                 s2 = [1,2,4]
        #                 s3 = [5]
        #                 basis = [s1,s2,s3]
        #             elif m >= 4:
        #                 s2 = [x for x in range(1,m)]
        #                 s3 = [x for x in range(m+1,2*m)]
        #                 basis = [s1,s2,s3]
        #         elif n in [4,5]:
        #             s1 = [x for x in range(0,m*n+1,m)]
        #             if m == 3:
        #                 s1.append(m*n-2)
        #                 s2 = [1,2,4]
        #                 s3 = []
        #                 for x in range(5,m*n):
        #                     if (x not in s1) and (x not in s2):
        #                         s3.append(x)
        #             elif m == 5:
        #                 s1 = []
        #                 s2 = []
        #                 s3 = []
        #             elif m == 9:
        #                 s1 = []
        #                 s2 = []
        #                 s3 = []
        #             elif m >= 4:
        #                 s1 = []
        #                 s2 = []
        #                 s3 = []
        #             basis = [s1,s2,s3]
        #     else:
        #         pd = int(n/2) + 1

        exec('self.pd_' + a + ' = pd')
        exec('self.basis_' + a + ' = basis')
        return g, title

    def graph_drawer(self, graph, position, ax, title):
        ''' Function to draw the updated graph into it's canvas '''

        ax.clear()
        ax.margins(0.2)
        ax.set_title(title)
        nx.draw(graph, position, with_labels=True, ax=ax, node_size=30)
        self.canvas.draw_idle()

    def graph_basis_updater(self, sender):
        ''' Function to update basis of the updated graph '''

        graph = sender.text()[-1].lower()
        b = eval('self.basis_' + graph)

        # set the basis
        if eval('self.' + graph + '.order()') == 1: # if the graph is trivial
            self.basis_text_updater(graph, [[0]])
        else:
            # 1 check whether the basis has already determined
            if b != [[0]] and b!= [[(0,0)]]:
                basis = b
            else: # if not, search the basis with brute force
                basis = eval('basis_search(self.' + graph + \
                             ', self.reverse, self.pd_' + \
                             graph + ')')

            # 2 send signal to change text in the result box
            self.basis_text_updater(graph, basis)

            # 3 update the graph canvas
            ax = eval('self.ax_' + graph)
            pos = eval('self.pos_' + graph)
            for i in range(len(basis)):
                nx.draw_networkx_nodes(graph, pos, ax = ax,
                                       nodelist = basis[i],
                                       node_size = 100,
                                       node_color = self.colors[i],
                                       label = 'B' + graph.upper() + str(i+1))
            ax.legend(scatterpoints=1, loc='best', fontsize='x-small')
            self.canvas.draw_idle()

        # disabling basis updater button after executed once
        eval('self.button_b' + graph + '.setEnabled(False)')
        exec('self.pd_' + graph + ' = 2')
        exec('self.basis_' + graph + ' = [[0]]')

    def basis_text_updater(self, graph, basis):
        ''' Function to update the text which shows the basis of a graph '''

        pd = len(basis)
        basis_pg = '' # initialize variable for basis text for display
        graph_ = graph.upper() # is this graph G, H, or P?

        # setting the basis text
        for i,b in enumerate(basis):
            basis_pg = basis_pg + 'B' + graph_ + str(i+1) \
                       + ' : {' + str(b)[1:-1] + '}\n'

        # setting the whole text
        b_text = 'Basis of ' + graph_ + ':\n' \
                + basis_pg \
                + 'pd(' + graph_ + ') = ' + str(pd)


        # get the representation
        g = eval('self.' + graph)
        r_ = r(g,basis)
        rep = ''
        for v in r_.keys():
            rep = rep + 'r(v_' + str(v) + ' | B' + graph_ + ') = ' \
                  + str(tuple(r_[v])) + '\n'
        b_text = b_text + '\nRepresentations of V(' + graph_ + '):\n' + rep \
                 + 'Resolving: ' + str(is_resolving(g,basis))

        # update the header text
        eval('self.header_b' + graph + '.setText(b_text)')

    def on_graph_g(self):
        ''' Function to set graph G '''

        graph_type = str(self.graph_g.currentText()) # what class is this graph?
        m = self.slider_gm.value() # read the first parameter (#vertex)
        n = self.slider_gn.value() # read the second parameter, if any

        # initialize the graph python class and it's title for display
        self.g, self.title_g = self.graph_generator(graph_type, m, n, 'g')
        self.pos_g = nx.spring_layout(self.g) # setting nodes position for display

        # call graph drawing function
        self.graph_drawer(self.g, self.pos_g, self.ax_g, 'G ='+self.title_g)

        # enabling basis updater button
        self.button_bg.setEnabled(True)

    def on_graph_h(self):
        ''' Function to set graph H '''

        graph_type = str(self.graph_h.currentText()) # what class is this graph?
        m = self.slider_hm.value() # read the first parameter (#nodes)
        n = self.slider_hn.value() # read the second parameter, if any

        # initialize the graph python class and it's title for display
        self.h, self.title_h = self.graph_generator(graph_type, m, n, 'h')
        self.pos_h = nx.spring_layout(self.h) # setting nodes position for display

        # call graph drawing function
        self.graph_drawer(self.h, self.pos_h, self.ax_h, 'H ='+self.title_h)

        # enabling basis updater button
        self.button_bh.setEnabled(True)

    def on_product(self):
        ''' Function to set graph P (product of G and H) and it's basis '''

        product = str(self.product.currentText()) # which product is selected?

        # if indeed G and H is set and a certain product is selected
        if (hasattr(self,'g') == True) and (hasattr(self,'h') == True) \
            and (product != '==No product==') and (product != ''):

            # initializing the variables
            g = str(self.graph_g.currentText())
            g_order = len(self.g.nodes())
            h = str(self.graph_h.currentText())
            h_order = len(self.h.nodes())
            G = {g:g_order, h:h_order}
            n = self.slider_p.value()
            pd, basis = 2, [[(0,0)]]

                # ROOTED PRODUCT
            if product == 'Rooted':
                self.p = eval(self.products[product][0] + '(self.g, self.h, 0)')
                if all(g == 'Path' for g in G.keys()) \
                    and all(v == 4 for v in G.values()):
                    pd = 3
            else:
                self.p = eval(self.products[product][0] + '(self.g, self.h)')

                # CARTESIAN PRODUCT
                if product == 'Cartesian':

                    # deteriminng the basis
                    if g == 'Path' and h == 'Path':
                        basis = [[(0,0)]]
                        basis.append([(i,0) for i in range(1,g_order)])
                        basis.append([(i,j) for i in range(g_order) \
                                            for j in range(1,h_order)])

                    elif 'Cycle' in G:
                        if 'Path' in G:
                            pass

                # N-STRONG PRODUCT
                elif product == 'N-Strong':

                    # initializing the graph, adding extra edges from cartesian product
                    d = nx.shortest_path_length
                    for u in self.p.nodes:
                        for v in self.p.nodes:
                            if d(self.g, u[0], v[0]) == n and \
                                d(self.h, u[1], v[1]) == n:
                                self.p.add_edge(u,v)

                    # determining the basis
                        # if it is n-strong graph but n is not 1
                    if n != 1:
                        pass

                        # if it is 1-strong graph, use basis from Yero
                    else:
                        # Jika Path dan Path
                        if g == 'Path' and h == 'Path' \
                            and (g_order >= 2 and h_order >= 2):
                            pd = 4
                            basis = [[(0,0)],
                                    [(0,i) for i in range(1,h_order)],
                                    [(i,0) for i in range(1,g_order)],
                                    [(i,j) for i in range(1,g_order) \
                                    for j in range(1,h_order)]]

                        elif 'Complete' in G:
                        # Jika Complete dan Path
                            if 'Path' in G:
                                if G['Path'] == 2:
                                    pd = 2 * G['Complete']
                                    basis = [[(i,j)] for i in range(g_order) \
                                                    for j in range(h_order)]
                                elif G['Path'] >= 3:
                                    pd = G['Complete'] + 2
                                    if g == 'Path':
                                        basis = [[(0,0)], [(1,0)],
                                                [(i,0) for i in range(2,g_order)],]
                                        basis.extend([[(i,j) for i in range(g_order)] \
                                                            for j in range(1,h_order)])
                                    else:
                                        basis = [[(0,0)], [(0,1)],
                                                [(0,i) for i in range(2,g_order)],]
                                        basis.extend([[(j,i) for i in range(g_order)] \
                                                            for j in range(1,h_order)])
                        # Jika Complete dan Cycle
                            elif 'Cycle' in G:
                                if G['Cycle'] >= 6:
                                    pd = G['Complete'] + 2
                                    if g_ == 'Cycle':
                                        b = [[(i,j) for i in range(g_order)] for j in range(1,h_order)]
                                        basis = [[(0,0)],[(1,0),(2,0)]]
                                        basis.append([(i,0) for i in range(3,g_order)])
                                        basis.extend(b)
                                    else:
                                        b = [[(j,i) for i in range(h_order)] for j in range(1,g_order)]
                                        basis = [[(0,0)],[(0,1),(0,2)]]
                                        basis.append([(0,i) for i in range(3,h_order)])
                                        basis.extend(b)
                                elif G['Cycle'] >= 4:
                                    pd = G['Complete'] + 3
                                    if g_ == 'Cycle':
                                        b = [[(i,j) for i in range(g_order)] for j in range(1,h_order)]
                                        basis = [[(i,0)] for i in range(4)]
                                        if g_order == 5: basis[-1].append((4,0))
                                    else:
                                        b = [[(j,i) for i in range(h_order)] for j in range(1,g_order)]
                                        basis = [[(0,i)] for i in range(4)]
                                        if h_order == 5: basis[-1].append((0,4))
                                    basis.extend(b)
                                elif G['Cycle'] == 3:
                                    pd = 3 * G['Complete']
                                    basis = [[(i,j)] for i in range(3) \
                                                    for j in range(G['Complete'])]
                        # Jika Complete dan Complete
                            elif g == 'Complete' and h == 'Complete':
                                pd = g_order * h_order
                                basis = [[(i,j)] for i in range(g_order) \
                                                for j in range(h_order)]
                            else:
                                pd = G['Complete'] + 2


                elif product == 'Comb':
                    pass

            self.pd_p = pd
            self.basis_p = basis
            self.title_p = self.title_g + self.products[product][1] + self.title_h
            self.pos_p = nx.spring_layout(self.p)
            self.graph_drawer(self.p, self.pos_p, self.ax_p, 'P ='+self.title_p)

            # enabling basis updater button
            self.button_bp.setEnabled(True)

    def disableWidget(self, currentIndex):
        if currentIndex not in ['==No product==','']:
            self.graph_h.setEnabled(True)
            self.slider_hm.setEnabled(True)
            self.slider_hn.setEnabled(True)
        else:
            self.graph_h.setEnabled(False)
            self.slider_hm.setEnabled(False)
            self.slider_hn.setEnabled(False)
            self.title_p = self.title_g
            self.ax_h.clear()
            self.ax_h.axis('off')
            self.ax_p.clear()
            self.ax_p.axis('off')
            self.canvas.draw_idle()

        sender = self.sender()
        if currentIndex in ['Lollipop', 'Complete Bipartite', 'Wheel (m-step)',
                            'Jahangir Generalised']:
            if sender is self.graph_g:
                self.slider_gn.setEnabled(True)
            if sender is self.graph_h:
                self.slider_hn.setEnabled(True)
        else:
            if sender is self.graph_g:
                self.slider_gn.setEnabled(False)
            if sender is self.graph_h:
                self.slider_hn.setEnabled(False)

        if currentIndex in ['N-Strong']:
            self.slider_p.setEnabled(True)
        else:
            self.slider_p.setEnabled(False)

    def center(self):
        qr = self.frameGeometry()
        cp = Widget.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def basis_search(g, reverse, pd_limit=2):

    def partition(Set, m):
        def visit(n, a):
            ps = [[] for i in range(m)]
            for j in range(n):
                ps[a[j + 1]].append(Set[j])
            return ps

        def f(mu, nu, sigma, n, a):
            if mu == 2:
                yield visit(n, a)
            else:
                for v in f(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                    yield v
            if nu == mu + 1:
                a[mu] = mu - 1
                yield visit(n, a)
                while a[nu] > 0:
                    a[nu] -= 1
                    yield visit(n, a)
            elif nu > mu + 1:
                if (mu + sigma) % 2 == 1:
                    a[nu - 1] = mu - 1
                else:
                    a[mu] = mu - 1
                if (a[nu] + sigma) % 2 == 1:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                while a[nu] > 0:
                    a[nu] -= 1
                    if (a[nu] + sigma) % 2 == 1:
                        for v in b(mu, nu - 1, 0, n, a):
                            yield v
                    else:
                        for v in f(mu, nu - 1, 0, n, a):
                            yield v

        def b(mu, nu, sigma, n, a):
            if nu == mu + 1:
                while a[nu] < mu - 1:
                    yield visit(n, a)
                    a[nu] += 1
                yield visit(n, a)
                a[mu] = 0
            elif nu > mu + 1:
                if (a[nu] + sigma) % 2 == 1:
                    for v in f(mu, nu - 1, 0, n, a):
                        yield v
                else:
                    for v in b(mu, nu - 1, 0, n, a):
                        yield v
                while a[nu] < mu - 1:
                    a[nu] += 1
                    if (a[nu] + sigma) % 2 == 1:
                        for v in f(mu, nu - 1, 0, n, a):
                            yield v
                    else:
                        for v in b(mu, nu - 1, 0, n, a):
                            yield v
                if (mu + sigma) % 2 == 1:
                    a[nu - 1] = 0
                else:
                    a[mu] = 0
            if mu == 2:
                yield visit(n, a)
            else:
                for v in b(mu - 1, nu - 1, (mu + sigma) % 2, n, a):
                    yield v

        n = len(Set)
        a = [0] * (n + 1)
        for j in range(1, m + 1):
            a[n - m + j] = j - 1
        return f(m, n, 0, n, a)

    def search_basis(g):
        pd_min = pd_limit
        pd_max = g.order()+1
        if reverse: # if the limit is meant to be upper-bound
            pd_max = pd_min
            pd_min = 2
        v = list(g)
        for k in range(pd_min,pd_max):
            all_p = partition(v,k)
            for p in all_p:
                if is_resolving(g,p):
                    return p

    if nx.is_connected(g):
        return search_basis(g)
    else:
        return None

def r(g, partitions):
    rep = {}
    for v in g.nodes:
        rep[v] = []
        for part in partitions:
            dist_vp = g.order()
            for w in part:
                d_vw = nx.shortest_path_length(g,v,w)
                if d_vw < dist_vp:
                    dist_vp = d_vw
            rep[v].append(dist_vp)
    return rep

def is_resolving(g, partitions):
        rep = r(g, partitions)
        rev_rep = {}
        for key, value in rep.items():
            rev_rep[str(value)] = key
        if len(rep) == len(rev_rep): return True
        else: return False

if __name__ == '__main__':
    import sys
    app = Widget.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle("Fusion")
    screen = MainProgram()
    screen.show()
    sys.exit(app.exec_())
