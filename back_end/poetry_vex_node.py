
class PoetryVexNode(object):
    def __init__(self, vex_id, name, themes, link, degree, clustering_coefficient, coreness):
        self.vex_id = vex_id  # int
        self.name = name  # str
        self.themes = themes  # str
        self.link = link  # str
        self.degree = degree  # int
        self.clustering_coefficient = clustering_coefficient  # float
        self.coreness = coreness  # int
        self.adjacent_vexes = []  # list of int
        self.adjacent_edges = []  # list of int

    def set_vex_id(self, vex_id):
        self.vex_id = vex_id

    def get_vex_id(self):
        return self.vex_id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_themes(self, themes):
        self.themes = themes

    def get_themes(self):
        return self.themes

    def set_link(self, link):
        self.link = link

    def get_link(self):
        return self.link

    def set_degree(self, degree):
        self.degree = degree

    def get_degree(self):
        return self.degree

    def set_clustering_coefficient(self, clustering_coefficient):
        self.clustering_coefficient = clustering_coefficient

    def get_clustering_coefficient(self):
        return self.clustering_coefficient

    def set_coreness(self, coreness):
        self.coreness = coreness

    def get_coreness(self):
        return self.coreness

    def add_adjacent_vexes(self, vex_id):
        self.adjacent_vexes.append(vex_id)

    def set_adjacent_vexes(self, vex_id_list):
        self.adjacent_vexes = vex_id_list

    def get_adjacent_vexes(self):
        return self.adjacent_vexes

    def add_adjacent_edges(self, edge_id):
        self.adjacent_edges.append(edge_id)

    def set_adjacent_edges(self, edge_id_list):
        self.adjacent_edges = edge_id_list

    def get_adjacent_edges(self):
        return self.adjacent_edges

