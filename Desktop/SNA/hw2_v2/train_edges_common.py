import networkx as nx

def generate_graph():
	G = nx.Graph()
	with open('train_edges.txt','r') as f:
		f.readline()
		f.readline()
		for data in f:
			G.add_edge(data.strip().split()[0],data.strip().split()[1])	
	return G		
def generate_common_neighbour(G):
	file_edges = open('train_edges_common.txt','w')
	with open('train_edges.txt','r') as f:
		f.readline()
		f.readline()
		for data in f:
			index = 0
			for i in nx.common_neighbors(G,data.strip().split()[0],data.strip().split()[1]):
				index += 1
			#print data.strip().split()[0],data.strip().split()[1],index
			#quit()
			file_edges.write(data.strip().split()[0]+' '+data.strip().split()[1]+' '+str(index)+'\n')
			#quit()
	file_edges.close()
def main():
	G = generate_graph()
	generate_common_neighbour(G)
if __name__ == '__main__':
	main()