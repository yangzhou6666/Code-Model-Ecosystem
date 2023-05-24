'''Visualize networks using Python'''

import os
import csv
import networkx as nx
import matplotlib.pyplot as plt


if __name__ == '__main__':
    data_path = 'data/manual-labeling.csv'

    model_set = set()
    dataset_set = set()
    model_data_pair = []
    with open(data_path, 'r', newline='',encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            model = row[0]
            dataset = row[1]
            if dataset == '':
                continue
            model_data_pair.append((model, dataset))
            model_set.add(model)
            dataset_set.add(dataset)


    G = nx.Graph()

    # add nodes
    for model in model_set:
        G.add_node(model)
    for dataset in dataset_set:
        G.add_node(dataset)
    
    # add edges
    for model, dataset in model_data_pair:
        G.add_edge(model, dataset)

    # 绘制图形
    nx.draw(G, with_labels=False, node_size=20)

    # 显示图形
    plt.show()