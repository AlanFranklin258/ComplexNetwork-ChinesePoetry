

def list_to_str(input_list):
    output_string = ''
    for i in range(len(input_list)-1):
        output_string += input_list[i] + '，'
    output_string += input_list[len(input_list)-1]
    return output_string


def get_formal_data(poetry_vex_node_list, poetry_edge_node_list):
    nodes_cache = []
    for i in range(len(poetry_vex_node_list)):
        label_name_list = poetry_vex_node_list[i].get_name().split('·')
        label_name = label_name_list[len(label_name_list) - 1]
        nodes_cache.append(
            (
                poetry_vex_node_list[i].get_name(),
                label_name,
                poetry_vex_node_list[i].get_themes(),
                poetry_vex_node_list[i].get_link(),
            )
        )
    nodes = [
        {
            'data': {
                'id': idd,
                'label': label,
                'themes': themes,
                'link': link,
            }
        }for idd, label, themes, link in tuple(nodes_cache)
    ]
    edges_cache = []
    for i in range(len(poetry_edge_node_list)):
        edges_cache.append(
            (
                poetry_edge_node_list[i].get_poetry1(),
                poetry_edge_node_list[i].get_poetry2(),
                list_to_str(poetry_edge_node_list[i].get_key_words()),
            )
        )
    edges = [
        {
            'data': {
                'source': source,
                'target': target,
                'label': label,
            }
        } for source, target, label in tuple(edges_cache)
    ]
    # for i in range(len(edges)):
    #     print(edges[i])

    return nodes + edges
