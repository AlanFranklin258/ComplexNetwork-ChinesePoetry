import xlrd2
import numpy as np

from back_end import poetry_vex_node
from back_end.poetry_edge_node import PoetryEdgeNode

""" 
本.py文件对于图的顶点结点和边结点有写操作的权限，其他模块对已经建构好的图只能有读的操作 
"""


# 根据路径读取表格，表格的形式须和自定义结点类充分一致
def read_poetry_data(xlsx_path):
    xlsx = xlrd2.open_workbook(xlsx_path)
    sheet = xlsx.sheet_by_name("诗经")
    poetry_vex_node_list = []
    for i in range(1, sheet.nrows):
        raw_data = sheet.row_values(i)
        # 初始图中，设置的顶点id一般等于list的序号
        pvn = poetry_vex_node.PoetryVexNode(i-1, raw_data[0], raw_data[1], raw_data[3], 0, raw_data[6], raw_data[7])
        poetry_vex_node_list.append(pvn)
    return poetry_vex_node_list


# 获取两个list的相交部分
def get_intersection(list1, list2):
    intersection_list = []
    for i in range(len(list1)):
        if list2.count(list1[i]) >= 1:
            intersection_list.append(list1[i])
    return intersection_list


# 根据vex结点生成edge结点
# 在此项目中，属性计算还是更多依赖邻接矩阵和vex结点信息
# edge结点主要是为了可视化展示，因此每次更新vex后，涉及到可视化，都需要调用这个函数
def get_edge_node_list(poetry_vex_node_list):
    # all_themes用于检索，暂时禁用
    # all_themes = []
    poetry_edge_node_list = []
    edge_id = 0
    # 以下属性需要重置
    for i in range(len(poetry_vex_node_list)):
        poetry_vex_node_list[i].set_degree(0)
        poetry_vex_node_list[i].set_adjacent_vexes([])
        poetry_vex_node_list[i].set_adjacent_edges([])
    for i in range(len(poetry_vex_node_list) - 1):
        for j in range(i + 1, len(poetry_vex_node_list)):
            themes1 = poetry_vex_node_list[i].get_themes()
            themes2 = poetry_vex_node_list[j].get_themes()
            if themes1 == '' or themes2 == '':
                continue
            # 注意，初始数据是中文的逗号
            themes1_list = themes1.split("，")
            themes2_list = themes2.split("，")
            intersection_list = get_intersection(themes1_list, themes2_list)
            # 建立edge结点
            if len(intersection_list) > 0:
                pen = PoetryEdgeNode(edge_id,
                                     "themes",
                                     poetry_vex_node_list[i].get_vex_id(),
                                     poetry_vex_node_list[i].get_name(),
                                     poetry_vex_node_list[j].get_vex_id(),
                                     poetry_vex_node_list[j].get_name(),
                                     intersection_list
                                     )
                poetry_edge_node_list.append(pen)
                # 更新vex的degree
                poetry_vex_node_list[i].set_degree(poetry_vex_node_list[i].get_degree() + 1)
                poetry_vex_node_list[j].set_degree(poetry_vex_node_list[j].get_degree() + 1)
                # 更新vex的邻接点
                # todo:实际上,修改vex结点的做法就是改变adjacent_vexes属性，尽管此处再重置一遍不会改变结果，但还是很浪费，有空想办法解耦一下
                poetry_vex_node_list[i].add_adjacent_vexes(poetry_vex_node_list[j].get_vex_id())
                poetry_vex_node_list[j].add_adjacent_vexes(poetry_vex_node_list[i].get_vex_id())
                # 更新vex的邻接边
                poetry_vex_node_list[i].add_adjacent_edges(edge_id)
                poetry_vex_node_list[j].add_adjacent_edges(edge_id)
                edge_id += 1
    return poetry_vex_node_list, poetry_edge_node_list


# 根据顶点结点生成邻接矩阵，方便最短路径、生成子图的计算
def get_adjacent_matrix(poetry_vex_node_list):
    length = len(poetry_vex_node_list)
    adjacent_matrix = np.zeros((length, length), int)
    for i in range(length):
        for j in range(length):
            if i == j:
                adjacent_matrix[i][j] = 0
            else:
                adjacent_matrix[i][j] = judge_adjacent_vex_to_vex(poetry_vex_node_list[i], poetry_vex_node_list[j])
    return adjacent_matrix


# 生成初始图
def get_graph():
    poetry_vex_node_list = read_poetry_data("D:\\PycharmProjects\\complexnetwork\\data\\poetries.xlsx")
    poetry_vex_node_list, poetry_edge_node_list = get_edge_node_list(poetry_vex_node_list)
    # for i in range(len(poetry_vex_node_list)):
    #     print(poetry_vex_node_list[i].get_degree())
    # for i in range(len(poetry_edge_node_list)):
    #     print(poetry_edge_node_list[i].get_edge_type()+" "+poetry_edge_node_list[i].get_poetry1()+" "
    #           + poetry_edge_node_list[i].get_poetry2()+" "+" ".join(poetry_edge_node_list[i].get_key_words()))
    return poetry_vex_node_list, poetry_edge_node_list


# 根据id搜索并返回vex结点
def search_vex_node_by_id(poetry_vex_node_list, vex_id):
    for i in range(len(poetry_vex_node_list)):
        if poetry_vex_node_list[i].get_vex_id() == vex_id:
            return poetry_vex_node_list[i]
    return None


# 根据id搜索并返回edge结点
def search_edge_node_by_id(poetry_edge_node_list, edge_id):
    for i in range(len(poetry_edge_node_list)):
        if poetry_edge_node_list[i].get_edge_id() == edge_id:
            return poetry_edge_node_list[i]
    return None


# 寻找两个vex结点的公共边id，没有则返回-1
def find_public_edge(poetry_vex_node1, poetry_vex_node2):
    edges1 = poetry_vex_node1.get_adjacent_edges()
    edges2 = poetry_vex_node2.get_adjacent_edges()
    for i in range(len(edges1)):
        for j in range(len(edges2)):
            if edges1[i] == edges2[j]:
                return edges1[i]
    return -1


# 根据邻接点属性，判断两个vex结点是否相邻
def judge_adjacent_vex_to_vex(poetry_vex_node1, poetry_vex_node2):
    vexes1 = poetry_vex_node1.get_adjacent_vexes()
    for i in range(len(vexes1)):
        if vexes1[i] == poetry_vex_node2.get_vex_id():
            return 1
    return 0


# 为计算clustering coefficient提供neighbours和neighbours之间的连接关系
def serve_clustering_coefficient(poetry_vex_node_list, poetry_edge_node_list, neighbour_id_list):
    neighbour_list = []
    for i in range(len(neighbour_id_list)):
        ref = search_vex_node_by_id(poetry_vex_node_list, neighbour_id_list[i])
        if ref is not None:
            neighbour_list.append(ref)
    neighbour_edge_list = []
    for i in range(len(neighbour_list) - 1):
        for j in range(i + 1, len(neighbour_list)):
            edge_id = find_public_edge(neighbour_list[i], neighbour_list[j])
            if edge_id != -1:
                ref = search_edge_node_by_id(poetry_edge_node_list, edge_id)
                if ref is not None:
                    neighbour_edge_list.append(ref)
    return neighbour_list, neighbour_edge_list


# 移除结点，更新adjacent_vexes和degree属性
def remove_poetry_vex_node(poetry_vex_node_list, delete_poetry_vex_node):
    adjacent_vexes = delete_poetry_vex_node.get_adjacent_vexes()
    poetry_vex_node_list.remove(delete_poetry_vex_node)
    for i in range(len(adjacent_vexes)):
        adjacent_vex_node = search_vex_node_by_id(poetry_vex_node_list, adjacent_vexes[i])
        if adjacent_vex_node is not None:
            poetry_vex_node_list.remove(adjacent_vex_node)

            adjacent_vexes2 = adjacent_vex_node.get_adjacent_vexes()
            adjacent_vexes2.remove(delete_poetry_vex_node.get_vex_id())
            adjacent_vex_node.set_adjacent_vexes(adjacent_vexes2)
            adjacent_vex_node.set_degree(adjacent_vex_node.get_degree() - 1)

            poetry_vex_node_list.append(adjacent_vex_node)
    return poetry_vex_node_list
