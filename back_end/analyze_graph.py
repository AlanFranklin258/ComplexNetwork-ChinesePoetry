import networkx as nx
import numpy as np

# 在读取表格构建顶点时，就计算了vex的degree值，此处只是做个统计，用于输出频数分布直方图和前十表格
from back_end.produce_graph import search_vex_node_by_id, remove_poetry_vex_node, serve_clustering_coefficient, \
    get_adjacent_matrix


# 按degree降序排列，用于可视化
def show_vex_node_by_degree_descending(poetry_vex_node_list):
    poetry_vex_node_name_array = []
    poetry_vex_node_themes_array = []
    poetry_vex_node_degree_array = []
    sort_list = []
    for i in range(len(poetry_vex_node_list)):
        sort_list.append(
            (
                poetry_vex_node_list[i].get_name(),
                poetry_vex_node_list[i].get_themes(),
                poetry_vex_node_list[i].get_degree()
            )
        )
    sort_list.sort(key=by_degree1, reverse=True)
    for i in range(len(sort_list)):
        poetry_vex_node_name_array.append(sort_list[i][0])
        poetry_vex_node_themes_array.append(sort_list[i][1])
        poetry_vex_node_degree_array.append(sort_list[i][2])

    return poetry_vex_node_name_array, poetry_vex_node_themes_array, poetry_vex_node_degree_array


def by_degree1(element):
    return element[2]


# 按clustering coefficient降序排列，用于可视化
def show_vex_node_by_clustering_coefficient_descending(poetry_vex_node_list):
    poetry_vex_node_name_array = []
    poetry_vex_node_themes_array = []
    poetry_vex_node_clustering_coefficient_array = []
    total_clustering_coefficient = 0.0
    sort_list = []
    for i in range(len(poetry_vex_node_list)):
        sort_list.append(
            (
                poetry_vex_node_list[i].get_name(),
                poetry_vex_node_list[i].get_themes(),
                poetry_vex_node_list[i].get_clustering_coefficient()
            )
        )
        total_clustering_coefficient += poetry_vex_node_list[i].get_clustering_coefficient()
    sort_list.sort(key=by_clustering_coefficient, reverse=True)
    for i in range(len(sort_list)):
        poetry_vex_node_name_array.append(sort_list[i][0])
        poetry_vex_node_themes_array.append(sort_list[i][1])
        poetry_vex_node_clustering_coefficient_array.append(sort_list[i][2])
    graph_clustering_coefficient = total_clustering_coefficient / len(poetry_vex_node_list)
    return poetry_vex_node_name_array, poetry_vex_node_themes_array, poetry_vex_node_clustering_coefficient_array, \
           graph_clustering_coefficient


def by_clustering_coefficient(element):
    return element[2]


# 按clustering coefficient降序排列，用于可视化
def show_vex_node_by_coreness_descending(poetry_vex_node_list):
    poetry_vex_node_name_array = []
    poetry_vex_node_themes_array = []
    poetry_vex_node_coreness_array = []
    sort_list = []
    for i in range(len(poetry_vex_node_list)):
        sort_list.append(
            (
                poetry_vex_node_list[i].get_name(),
                poetry_vex_node_list[i].get_themes(),
                poetry_vex_node_list[i].get_coreness()
            )
        )
    sort_list.sort(key=by_coreness, reverse=True)
    for i in range(len(sort_list)):
        poetry_vex_node_name_array.append(sort_list[i][0])
        poetry_vex_node_themes_array.append(sort_list[i][1])
        poetry_vex_node_coreness_array.append(sort_list[i][2])
    graph_coreness = sort_list[0][2]
    return poetry_vex_node_name_array, poetry_vex_node_themes_array, poetry_vex_node_coreness_array, graph_coreness


def by_coreness(element):
    return element[2]


# 根据邻接矩阵生成最大子图的vex集合
def get_maximal_connected_sub_graph(adjacent_matrix):
    G = nx.Graph()
    G.add_nodes_from(range(len(adjacent_matrix)))
    for i in range(len(adjacent_matrix)):
        for j in range(len(adjacent_matrix)):
            if adjacent_matrix[i][j] == 1:
                G.add_edge(i, j)
    max_cc = max(nx.algorithms.components.connected_components(G), key=len)
    return max_cc


# 计算最大连通分量的平均最短路径长度
def compute_average_shortest_path_length(adjacent_matrix):
    length = len(adjacent_matrix)
    G = nx.Graph()
    G.add_nodes_from(range(len(adjacent_matrix)))
    for i in range(length - 1):
        for j in range(i + 1, length):
            if adjacent_matrix[i][j] == 1:
                G.add_edge(i, j)
    total_length = 0
    division = length * (length - 1) / 2
    for i in range(length - 1):
        for j in range(i + 1, length):
            try:
                total_length += nx.dijkstra_path_length(G, source=i, target=j)
            except nx.NetworkXNoPath:
                division -= 1
    print(division)
    aspl = float(total_length / division)
    return aspl


"""
一些计算量太大，或者不需要根据生成子图动态计算的指标，可选择预先计算，作为顶点结点的属性存入表中
"""


# 计算clustering_coefficient
def compute_clustering_coefficient(poetry_vex_node_list, poetry_edge_node_list):
    c = []
    for i in range(len(poetry_vex_node_list)):
        neighbours = poetry_vex_node_list[i].get_adjacent_vexes()
        if len(neighbours) > 1:
            neighbour_list, neighbour_edge_list = serve_clustering_coefficient(poetry_vex_node_list,
                                                                               poetry_edge_node_list,
                                                                               neighbours)
            e = len(neighbour_list)
            k = len(neighbour_edge_list)
            ci = float(2 * e / k / (k - 1))
            # print(str(e) + ' ' + str(len(neighbours)) + ' ' + str(len(sub_poetry_vex_node_list)) + ' ' + str(ci))
            c.append(ci)
            print(ci)
        else:
            print(0.0)
            c.append(0.0)
    return sum(c) / len(c)


# 按degree升序排列，用于计算coreness
def get_vex_node_by_degree_ascending(poetry_vex_node_list):
    poetry_vex_node_id_array = []
    poetry_vex_node_name_array = []
    poetry_vex_node_degree_array = []
    sort_list = []
    for i in range(len(poetry_vex_node_list)):
        sort_list.append(
            (
                poetry_vex_node_list[i].get_vex_id(),
                poetry_vex_node_list[i].get_name(),
                poetry_vex_node_list[i].get_degree()
            )
        )
    sort_list.sort(key=by_degree2)
    for i in range(len(sort_list)):
        poetry_vex_node_id_array.append(sort_list[i][0])
        poetry_vex_node_name_array.append(sort_list[i][1])
        poetry_vex_node_degree_array.append(sort_list[i][2])
    return poetry_vex_node_id_array, poetry_vex_node_name_array, poetry_vex_node_degree_array


def by_degree2(element):
    return element[2]


# 计算coreness
def compute_coreness(poetry_vex_node_list, coreness, coreness_list):
    if len(poetry_vex_node_list) == 0:
        return coreness_list
    poetry_vex_node_id_array, poetry_vex_node_name_array, poetry_vex_node_degree_array = \
        get_vex_node_by_degree_ascending(poetry_vex_node_list)
    delete_vex_node_id = []
    for i in range(len(poetry_vex_node_degree_array)):
        if i == 0 or poetry_vex_node_degree_array[i] == poetry_vex_node_degree_array[i - 1]:
            delete_vex_node_id.append(poetry_vex_node_id_array[i])
        else:
            break
    for i in range(len(delete_vex_node_id)):
        delete_poetry_vex_node = search_vex_node_by_id(poetry_vex_node_list, delete_vex_node_id[i])
        if delete_poetry_vex_node is not None:
            poetry_vex_node_list = remove_poetry_vex_node(poetry_vex_node_list, delete_poetry_vex_node)
            coreness_list.append((delete_poetry_vex_node.get_vex_id(), coreness))
    return compute_coreness(poetry_vex_node_list, coreness + 1, coreness_list)


# 模拟随机攻击，计算生成子图结点数和最大连通分量的aspl，如果attack_ratio=0则退化为计算初始图的子图和连通分量
def random_attack(poetry_vex_node_list, attack_round):
    length = len(poetry_vex_node_list)
    attack_ratio = length // attack_round
    adjacent_matrix = get_adjacent_matrix(poetry_vex_node_list)
    for i in range(0, attack_round + 1):
        print('attack round: ' + str(i))
        for j in range(attack_ratio * i):
            target_id = np.random.randint(0, len(adjacent_matrix))
            adjacent_matrix = np.delete(adjacent_matrix, target_id, axis=0)
            adjacent_matrix = np.delete(adjacent_matrix, target_id, axis=1)
        max_node_set_of_connected_sub_graph = get_maximal_connected_sub_graph(adjacent_matrix)
        print(len(max_node_set_of_connected_sub_graph))
        aspl = compute_average_shortest_path_length(adjacent_matrix)
        print(aspl)
        adjacent_matrix = get_adjacent_matrix(poetry_vex_node_list)


# 模拟靶向攻击，按degree值降序剔除vex结点
def intentional_attack(poetry_vex_node_list, attack_round):
    poetry_vex_node_id_array = target_vex_node_by_degree_descending(poetry_vex_node_list)
    new_poetry_vex_node_list = []
    for i in range(len(poetry_vex_node_id_array)):
        new_poetry_vex_node_list.append(search_vex_node_by_id(poetry_vex_node_list, poetry_vex_node_id_array[i]))
    length = len(new_poetry_vex_node_list)
    attack_ratio = length // attack_round
    adjacent_matrix = get_adjacent_matrix(new_poetry_vex_node_list)
    for i in range(0, attack_round + 1):
        print('attack round: ' + str(i))
        for j in range(attack_ratio * i):
            adjacent_matrix = np.delete(adjacent_matrix, 0, axis=0)
            adjacent_matrix = np.delete(adjacent_matrix, 0, axis=1)
        max_node_set_of_connected_sub_graph = get_maximal_connected_sub_graph(adjacent_matrix)
        print(len(max_node_set_of_connected_sub_graph))
        aspl = compute_average_shortest_path_length(adjacent_matrix)
        print(aspl)
        adjacent_matrix = get_adjacent_matrix(new_poetry_vex_node_list)


# 按degree降序排列，用于计算intentional attack
def target_vex_node_by_degree_descending(poetry_vex_node_list):
    poetry_vex_node_id_array = []
    sort_list = []
    for i in range(len(poetry_vex_node_list)):
        sort_list.append(
            (
                poetry_vex_node_list[i].get_vex_id(),
                poetry_vex_node_list[i].get_degree()
            )
        )
    sort_list.sort(key=by_degree3, reverse=True)
    for i in range(len(sort_list)):
        poetry_vex_node_id_array.append(sort_list[i][0])
    return poetry_vex_node_id_array


def by_degree3(element):
    return element[1]
