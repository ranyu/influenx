import networkx as nx
import re

def generate_graph():
	G = nx.Graph()
	with open('train_edges.txt','r') as f:
		f.readline()
		f.readline()
		for data in f:
			G.add_edge(data.strip().split()[0],data.strip().split()[1])	
	return G		
def generate_common_neighbour(G):
	edges_list = []
	file_edges = open('train_edges_common_3.txt','w')
	with open('edges_new.txt','r') as f_edges:
		for data in f_edges:
			edges_list.append(data.strip())
	with open('train_edges.txt','r') as f:
		f.readline()
		f.readline()
		for data in f:
			node1 = data.strip().split()[0]
			node2 = data.strip().split()[1]
			index = 0
			preds = nx.jaccard_coefficient(G, [(node1,node2)])
			for u,v,p in preds:
				file_edges.write(node1+' '+node2+' '+str(p)+'\n')
			'''for i in nx.common_neighbors(G,node1,node2):
				index += 1'''

			#file_edges.write(node1+' '+node2+' '+str(index)+'\n')
	file_edges.close()	

def main():
	G = generate_graph()
	generate_common_neighbour(G)
if __name__ == '__main__':
	main()