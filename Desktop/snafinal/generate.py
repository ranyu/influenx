#!/usr/bin/env python
# encoding: utf-8

from igraph import Graph
import glob, os


def create_egonet(user_id):
    g = Graph(0)
    g.add_vertices(user_id)
    egonet_file = 'egonets/' + user_id + '.egonet'
    with open(egonet_file, 'r') as f:
        for line in f:
            line = line.rstrip().split(' ')
            neighbor = line[0].replace(':', '')
            if neighbor not in g.vs['name']:
                g.add_vertices(neighbor)
            for node in line[1:]:
                update_graph(g, neighbor, node)
    g.delete_vertices(0)
    return g.simplify()

def update_graph(graph, node1, node2):
    """add edges between node1 and node2 in graph"""
    if node2 not in graph.vs['name']:
        graph.add_vertices(node2)
    node1_idx = graph.vs.find(node1)
    node2_idx = graph.vs.find(node2)
    graph.add_edge(node1_idx, node2_idx)

def get_train_test_user():
    train_list = []
    user_list = []
    for infile in glob.glob('Training/*.circles'):
        infile_name = os.path.basename(infile).split('.')[0]
        train_list.append(infile_name)
    for infile in glob.glob('egonets/*.egonet'):
        infile_name = os.path.basename(infile).split('.')[0]
        user_list.append(infile_name)
    test_list = list(set(user_list) - set(train_list))
    return train_list, test_list

def read_circles(user_id):
    circles = {}
    circle_file = 'Training/' + user_id + '.circles'
    with open(circle_file, 'r') as f:
        line = f.readlines()
    for l in line:
        content = l.rstrip().split(' ')
        k = content[0].replace(':', '')
        circles[k] = content[1:]
    return circles


train_list,test_list = get_train_test_user()
#print train_list,test_list
#print read_circles('7667')
print create_egonet('22364')

