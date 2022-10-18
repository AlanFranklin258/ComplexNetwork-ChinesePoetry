class PoetryEdgeNode(object):
    def __init__(self, edge_id, edge_type, poetry1_id, poetry1, poetry2_id, poetry2, key_words):
        self.edge_id = edge_id  # int
        self.edge_type = edge_type  # str
        self.poetry1_id = poetry1_id  # int
        self.poetry1 = poetry1  # str
        self.poetry2_id = poetry2_id  # int
        self.poetry2 = poetry2  # str
        self.key_words = key_words  # list of str

    def set_edge_id(self, edge_id):
        self.edge_id = edge_id

    def get_edge_id(self):
        return self.edge_id

    def set_edge_type(self, edge_type):
        self.edge_type = edge_type

    def get_edge_type(self):
        return self.edge_type

    def set_poetry1_id(self, poetry1_id):
        self.poetry1_id = poetry1_id

    def get_poetry1_id(self):
        return self.poetry1_id

    def set_poetry1(self, poetry1):
        self.poetry1 = poetry1

    def get_poetry1(self):
        return self.poetry1

    def set_poetry2_id(self, poetry2_id):
        self.poetry2_id = poetry2_id

    def get_poetry2_id(self):
        return self.poetry2_id

    def set_poetry2(self, poetry2):
        self.poetry2 = poetry2

    def get_poetry2(self):
        return self.poetry2

    def set_key_words(self, key_words):
        self.key_words = key_words

    def get_key_words(self):
        return self.key_words
