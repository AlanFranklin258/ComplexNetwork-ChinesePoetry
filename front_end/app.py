import dash_cytoscape as cyto
import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

from back_end.analyze_graph import show_vex_node_by_degree_descending, \
    show_vex_node_by_clustering_coefficient_descending, show_vex_node_by_coreness_descending
from back_end.pre_process_graph import get_formal_data
from back_end.produce_graph import get_graph

app = Dash(external_stylesheets=[dbc.themes.VAPOR])

colors = {
    'background': '#111111',
    'text': '#FFFFFF'
}

# 拓扑图可视化数据准备
poetry_vex_node_list, poetry_edge_node_list = get_graph()
elements = get_formal_data(poetry_vex_node_list, poetry_edge_node_list)
# degree分布可视化数据准备
poetry_vex_node_name_array1, poetry_vex_node_themes_array1, poetry_vex_node_degree_array \
    = show_vex_node_by_degree_descending(poetry_vex_node_list)
# clustering coefficient分布可视化数据准备
poetry_vex_node_name_array2, poetry_vex_node_themes_array2, poetry_vex_node_clustering_coefficient_array, \
graph_clustering_coefficient = show_vex_node_by_clustering_coefficient_descending(poetry_vex_node_list)
# coreness分布可视化数据准备
poetry_vex_node_name_array3, poetry_vex_node_themes_array3, poetry_vex_node_coreness_array, graph_coreness \
    = show_vex_node_by_coreness_descending(poetry_vex_node_list)
# 序号
index_array = []
for i in range(len(poetry_vex_node_list)):
    index_array.append(i + 1)
# attack折线图可视化数据准备
df_line_chart_sub = pd.read_csv("D:\\PycharmProjects\\complexnetwork\\data\\attack_result_sub.csv")
df_line_chart_asp = pd.read_csv("D:\\PycharmProjects\\complexnetwork\\data\\attack_result_asp.csv")

app.layout = html.Div(
    # style={'backgroundColor': 'rgba(0,0,0,0)'},
    children=[
        html.H3(
            style={
                'textAlign': 'center',
                # 'color': colors['text'],
                'margin-top': '30px',
            },
            children='复杂网络-诗经研究',
        ),
        dbc.Tabs(
            [
                dbc.Tab(
                    dbc.Card(
                        dbc.CardBody(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        cyto.Cytoscape(
                                            id='cytoscape-event-callbacks',
                                            elements=elements,
                                            style={
                                                'width': '100%',
                                                'height': '600px',
                                                'backgroundColor': '#FFFFFF'
                                            },
                                            layout={
                                                'name': 'concentric',
                                                'padding': 30,
                                                'minNodeSpacing': 200,
                                            },
                                            stylesheet=[
                                                {
                                                    'selector': 'node',
                                                    'style': {
                                                        'label': 'data(label)',
                                                        'color': '#000000',
                                                        'backgroundColor': '#000000',
                                                    }
                                                },
                                                {
                                                    'selector': 'edge',
                                                    'style': {
                                                        # 'label': 'data(label)',
                                                        # 'color': '#FFFFFF'
                                                    }
                                                }
                                            ],
                                        ),
                                        width=8
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Row(
                                                dcc.Markdown(
                                                    id='cytoscape-tapNodeData-output-markdown',
                                                    style={
                                                        'color': '#000000',
                                                    }
                                                ),
                                                style={
                                                    'height': '290px',
                                                    'backgroundColor': '#FDF5E6',
                                                }
                                            ),
                                            dbc.Row(
                                                dcc.Markdown(
                                                    id='cytoscape-tapEdgeData-output-markdown',
                                                    style={
                                                        'color': '#000000',
                                                    }
                                                ),
                                                style={
                                                    'height': '290px',
                                                    'margin-top': '20px',
                                                    'backgroundColor': '#FDF5E6',
                                                }
                                            )
                                        ],
                                        width=4,
                                    ),
                                ]
                            )
                        )
                    ),
                    label="Topology",
                ),
                dbc.Tab(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    html.H4(
                                        style={
                                            'textAlign': 'center',
                                            'color': colors['text'],
                                            'margin-top': '30px',
                                        },
                                        children='Distribution of Degree',
                                    ),
                                ),
                                dbc.Row(
                                    dcc.Graph(
                                        figure=go.Figure(
                                            data=[
                                                go.Histogram(
                                                    x=poetry_vex_node_degree_array,
                                                    xbins={
                                                        'start': 0,
                                                        'end': len(poetry_vex_node_degree_array),
                                                        'size': 5,
                                                    },
                                                    name='Distribution of Degree'
                                                )
                                            ]
                                        )
                                    )
                                ),
                                dbc.Row(
                                    html.H4(
                                        style={
                                            'textAlign': 'center',
                                            'color': colors['text'],
                                            'margin-top': '30px',
                                        },
                                        children='Top-10 Degree Poetries',
                                    ),
                                ),
                                dbc.Row(
                                    dbc.Table.from_dataframe(
                                        pd.DataFrame(
                                            {
                                                '序号': index_array,
                                                '诗歌名': poetry_vex_node_name_array1,
                                                '主题': poetry_vex_node_themes_array1,
                                                '度数': poetry_vex_node_degree_array,
                                            }
                                        ),
                                        striped=True,
                                        bordered=True,
                                        hover=True,
                                    )
                                )
                            ]
                        )
                    ),
                    label="Degree",
                ),
                dbc.Tab(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    html.H4(
                                        style={
                                            'textAlign': 'center',
                                            'color': colors['text'],
                                            'margin-top': '30px',
                                        },
                                        children='Distribution of Clustering Coefficient',
                                    ),
                                ),
                                dbc.Row(
                                    dcc.Graph(
                                        figure=go.Figure(
                                            data=[
                                                go.Histogram(
                                                    x=poetry_vex_node_clustering_coefficient_array,
                                                    xbins={
                                                        'start': 0,
                                                        'end': len(poetry_vex_node_clustering_coefficient_array),
                                                        'size': 0.01,
                                                    },
                                                    name='Distribution of Clustering Coefficient'
                                                )
                                            ]
                                        )
                                    )
                                ),
                                dbc.Row(
                                    html.H5(
                                        style={
                                            'textAlign': 'center',
                                            'color': colors['text'],
                                            'margin-top': '10px',
                                        },
                                        children='全图的Clustering Coefficient=' + str(graph_clustering_coefficient),
                                    ),
                                ),
                                dbc.Row(
                                    html.H4(
                                        style={
                                            'textAlign': 'center',
                                            'color': colors['text'],
                                            'margin-top': '30px',
                                        },
                                        children='Top-10 Clustering Coefficient Poetries',
                                    ),
                                ),
                                dbc.Row(
                                    dbc.Table.from_dataframe(
                                        pd.DataFrame(
                                            {
                                                '序号': index_array,
                                                '诗歌名': poetry_vex_node_name_array2,
                                                '主题': poetry_vex_node_themes_array2,
                                                '集聚系数': poetry_vex_node_clustering_coefficient_array,
                                            }
                                        ),
                                        striped=True,
                                        bordered=True,
                                        hover=True,
                                    )
                                )
                            ]
                        )
                    ),
                    label="Clustering Coefficient",
                ),
                dbc.Tab(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    html.H4(
                                        style={
                                            'textAlign': 'center',
                                            'color': colors['text'],
                                            'margin-top': '30px',
                                        },
                                        children='Distribution of Coreness',
                                    ),
                                ),
                                dbc.Row(
                                    dcc.Graph(
                                        figure=go.Figure(
                                            data=[
                                                go.Histogram(
                                                    x=poetry_vex_node_coreness_array,
                                                    xbins={
                                                        'start': 0,
                                                        'end': len(poetry_vex_node_coreness_array),
                                                        'size': 1,
                                                    },
                                                    name='Distribution of Coreness'
                                                )
                                            ]
                                        )
                                    )
                                ),
                                dbc.Row(
                                    html.H5(
                                        style={
                                            'textAlign': 'center',
                                            'color': colors['text'],
                                            'margin-top': '10px',
                                        },
                                        children='全图的Coreness=' + str(graph_coreness),
                                    ),
                                ),
                                dbc.Row(
                                    html.H4(
                                        style={
                                            'textAlign': 'center',
                                            'color': colors['text'],
                                            'margin-top': '30px',
                                        },
                                        children='Top-10 Coreness Poetries',
                                    ),
                                ),
                                dbc.Row(
                                    dbc.Table.from_dataframe(
                                        pd.DataFrame(
                                            {
                                                '序号': index_array,
                                                '诗歌名': poetry_vex_node_name_array3,
                                                '主题': poetry_vex_node_themes_array3,
                                                '核数': poetry_vex_node_coreness_array,
                                            }
                                        ),
                                        striped=True,
                                        bordered=True,
                                        hover=True,
                                    )
                                )
                            ]
                        )
                    ),
                    label="Coreness",
                ),
                dbc.Tab(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    html.H4(
                                        style={
                                            'textAlign': 'center',
                                            'color': colors['text'],
                                            'margin-top': '30px',
                                        },
                                        children='Comparison of Size of Connected Subgraph while attack for 20 times',
                                    ),
                                ),
                                dbc.Row(
                                    dcc.Graph(
                                        id="attack_line_chart_sub",
                                        figure=px.line(df_line_chart_sub,
                                                       x="ratio",
                                                       y="max_sub",
                                                       color='attack_way_sub',
                                                       markers=True)
                                    )
                                ),
                                dbc.Row(
                                    html.H4(
                                        style={
                                            'textAlign': 'center',
                                            'color': colors['text'],
                                            'margin-top': '30px',
                                        },
                                        children='Comparison of ASP while attack for 20 times',
                                    ),
                                ),
                                dbc.Row(
                                    dcc.Graph(
                                        id="attack_line_chart_asp",
                                        figure=px.line(df_line_chart_asp,
                                                       x="ratio",
                                                       y="max_asp",
                                                       color='attack_way_asp',
                                                       markers=True)
                                    )
                                ),
                            ]
                        )
                    ),
                    label="Attack",
                ),
            ]
        ),
    ])


@app.callback(Output('cytoscape-tapNodeData-output-markdown', 'children'),
              Input('cytoscape-event-callbacks', 'tapNodeData'), )
def displayTapNodeData(data):
    if data:
        return \
            "诗歌名：《" + data['id'] + "》\n\n" + "主题：" + data['themes'] + "\n\n" + "[原文链接](" + data['link'] + ")"


@app.callback(Output('cytoscape-tapEdgeData-output-markdown', 'children'),
              Input('cytoscape-event-callbacks', 'tapEdgeData'))
def displayTapEdgeData(data):
    if data:
        return "《" + data['source'] + "》与《" + data['target'] + "》\n\n" + "关联主题：" + data['label']


if __name__ == '__main__':
    app.run_server(debug=True)
