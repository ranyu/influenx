import networkx as nx

def simpath_spread(S,eta,U,G):
        Sigma = 0	# Initilize the Sigma
	result = 0
	V = G.nodes()	# V is all nodes set
	spd_dict = {}	# D[x] maintains the out-neighbors of x
	for j in G.nodes():
		spd_dict[j] = {}
	for k in G.nodes():
		for p in G.nodes():
			spd_dict[k][p] = 0	#Initilize the Edge Weight Value
	for u in S:
		temp = set(V) - set(S)	# V minus S
		temp.add(u)	# V minus S append u
		[result,spd_dict] = back_track(u,eta,temp,U,G,spd_dict)
		#Sigma += Sigma	# Each node in S calls BackTrack
		Sigma += result
	return Sigma,spd_dict
def back_track(u,eta,W,U,G,spd_dict):
	b = G.edge
	Q  = list()	# Stack that maintain the current nodes on the path
    # Initilize the Q,spd,pp and D
	Q.append(u)
	spd = 1
	pp = 1 	# Maintain the weight of the current path
 	# Produce D
	D = {}	# D[x] maintains the out-neighbors of x
	for i in G.nodes():
		D[i] = []
	while Q:
		[Q,D,spd,pp,spd_dict] = forward(Q,D,spd,spd_dict,pp,eta,W,U,G,b,u)
		u = Q.pop()		
		#print ('D',u,spd,pp)
		if Q:	# When the Q is Null,stop the process
			v = Q[-1]
			pp = float(pp)/ b[v][u]['influence']
		#print (b[v][u],pp)
	return spd,spd_dict
def forward(Q,D,spd,spd_dict,pp,eta,W,U,G,b,u):
	x  = Q[-1]
	pp = 0
	flag = True
	v = ''
	s = ''
	while flag:
		ys = G.successors(x)
		if len(ys) == 0:
			flag = False
			break
		while len(ys) > 0:
			y = ys[i]
			i += 1
			if y not in Q and y not in D[x] and y in W:	# y is not included in Q and Dx 
				if pp * b[x][y]['influence'] < eta:
					D[x].append(y)
				else:
					Q.append(y)
					print Q
					pp *= b[x][y]['influence']
					spd += pp
					D[x].append(y)	# Add y to x
					x = Q[-1]
					#print U
					for v in U:
						if v not in Q:
							#print 'v=',v,W-set(v)
							for s in W - set(v):
								#print W - set(v)
								#print 'w',W - set(v),s,u,spd_dict[s][u]
								spd_dict[s][u] += pp
								#print 'ss',spd_dict[s][u]
					print 'value',spd,pp
					i = 0
					break			
			if i == len(ys):
				flag = False
				#print 'here',spd_dict
				break
	return Q,D,spd,pp,spd_dict


def read_graph(filename):
	G = nx.DiGraph()
	G.add_edge('0','1',influence = .1)
	G.add_edge('1','2',influence = .4)
	G.add_edge('2','5',influence = .5)
	G.add_edge('2','3',influence = .5)
	G.add_edge('0','3',influence = .4)
	G.add_edge('3','0',influence = .8)
	G.add_edge('3','4',influence = .2)
	G.add_edge('4','1',influence = .2)
	G.add_edge('4','5',influence = .7)
	G.add_edge('5','6',influence = .8)
	G.add_edge('5','7',influence = .3)
	G.add_edge('6','7',influence = .1)
	G.add_edge('7','2',influence = .7)
	'''G.add_edge('x','y',influence = .3)
	G.add_edge('x','z',influence = .4)
	G.add_edge('y','x',influence = .1)
	G.add_edge('y','z',influence = .2)
	G.add_edge('z','y',influence = .5)
	G.add_edge('x','x',influence = 1.)
	G.add_edge('y','y',influence = 1.)
	G.add_edge('z','z',influence = 1.)
	G.add_edge('a','a',influence = 1.)
	G.add_edge('a','x',influence = .5)
	#G.add_edge('x','x',influence = 1.)
	#G.add_edge('y','y',influence = 1.)
	#G.add_edge('z','z',influence = 1.)
	#G.add_edge('a','a',influence = 1.)
	file_edge = open("partB_egofb_lt_edges.txt","r")
	file_node = open("partB_egofb_lt_nodes.txt","r")     
	text = file_edge.readline()
	text = file_edge.readline()
	for text in file_edge:
	    a = text.split()
	    G.add_edge(a[0],a[1],influence = float(a[2]))
	i = file_node.readline()
	for i in file_node:
	    a = i.split()
	    G.add_node(str(a[0]),threshold = float(a[1]))'''
	return G
def main():
	G = read_graph('')
	# Initilize the value
	S = ['0']	# Start seed
	eta = 0
	U = []
	pp = []
	ssss = 1
	sum = 1
	#pp = simpath_spread(S,eta,U,G)
	for s in set(G.nodes())-set(S):
		for x in nx.all_simple_paths(G,S[0],s):
			print x
			for p in xrange(len(x)-1):
				ssss = ssss * G.edge[x[p]][x[p+1]]['influence']
			sum += ssss
			print 'sum',sum
			ssss = 1
	print sum
	#print (pp[0])
if __name__ == '__main__':
	main()