import networkx as nx
import numpy as np

from back_end.analyze_graph import random_attack, intentional_attack
from back_end.produce_graph import get_graph


def by_id(element):
    return element[0]


if __name__ == '__main__':
    poetry_vex_node_list, poetry_edge_node_list = get_graph()
    # 提前计算clustering coefficient
    # c = compute_clustering_coefficient(poetry_vex_node_list, poetry_edge_node_list)
    # 提前计算coreness
    # coreness_list = []
    # coreness_list = compute_coreness(poetry_vex_node_list, 0, coreness_list)
    # coreness_list.sort(key=by_id)
    # for i in range(len(coreness_list)):
    #     print(coreness_list[i][1])
    # 提前计算random attack
    print('random attack')
    random_attack(poetry_vex_node_list, 20)
    print('intentional attack')
    intentional_attack(poetry_vex_node_list, 20)
