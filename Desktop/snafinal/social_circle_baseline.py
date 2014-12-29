import os
import collections
from read_test_set import read_test_set

from igraph import Graph

def deal_with_punc(sentence,punc):
	split = sentence.strip().split(punc)
	split_name = ''
	#print split
	for s in xrange(len(split)-1):
		split_name += split[s]+'_'
	return split_name,split[-1]

def get_filename(rootDir): 
    document_dir = []
    for lists in os.listdir(rootDir): 
        path = os.path.join(rootDir, lists) 
        document_dir.append(lists)
        if os.path.isdir(path): 
            get_filename(path)
    return document_dir

def loadFeatures(filename):
    featureMap = collections.defaultdict(dict)
    for line in open(filename):
        parts = line.strip().split()
        currentPerson = parts[0]
        for part in parts[1:]:
            key = part[0:part.rfind(';')]
            value = part[part.rfind(';')+1:]
            featureMap[currentPerson][key] = value
    #print featureMap['27519']
    return featureMap
def input_graph_data(featureMap,seed,test_set):
	feature_list = []
	with open('featureList.txt','r') as f:
		for data in f:
			feature_list.append(data.strip())
	g = Graph(directed = False)
	data = test_set.strip().split()
	#print data
	if seed not in g.vs:
		g.add_vertex(seed,birthday = featureMap[seed].get('birthday',0),education_classes_description = featureMap[seed].get(feature_list[1],0)\
				,education_classes_from_id = featureMap[seed].get(feature_list[2],0),education_classes_from_name = featureMap[seed].get(feature_list[3],0))
	for other_node in data:		
		if other_node not in g.vs:
			g.add_vertex(other_node, birthday = featureMap[other_node].get('birthday',0),education_classes_description = featureMap[other_node].get(feature_list[1],0)\
				,education_classes_from_id = featureMap[other_node].get(feature_list[2],0),education_classes_from_name = featureMap[other_node].get(feature_list[3],0))
			g.add_edge(seed,other_node)
	return g.simplify()
						#edges.append((node,other_node))
			#quit()
def extract_clusters(clusters, reverseIdMap):
    new_clusters = []
    for i in range(len(clusters)):
        next_cluster = [reverseIdMap[j] for j in clusters[i]]
        new_clusters.append(next_cluster)
    return new_clusters
def write_submission(node,cl):
	with open(node+'.circles','w') as f:
		for i in cl:
			f.write('circle:')
			for j in i:
				f.write(str(j)+' ')
			f.write('\n')
def main():	
	#edges = []
	test_set = read_test_set()
	featureMap = loadFeatures('features.txt')
	document_dir = get_filename('egonets')
	reverseIdMap = {}
	idMap = {}
	test_file_number = open('test_file_number.txt','w+')
	'''for i in test_set.keys():
		currentId = 0
		test_file_number.write(i+'\n')
	quit()'''
	for i in test_set.keys():
		currentId = 0
		#test_file_number.write(i)
		#quit()
		g = input_graph_data(featureMap,i,test_set[i])
		for friend in g.vs['name']:
			idMap[friend] = currentId
			reverseIdMap[currentId] = friend
			currentId += 1
		#dendogram = g.community_walktrap(steps=1)
		#cl = dendogram.as_clustering()
		#print 'GG',g
		#print 'TT',list(cl)
		#quit()
		dendogram = g.community_infomap(trials=10)
		#cl = dendogram.as_clustering()
		print dendogram
		#quit()
		#infomap_clusters = extract_clusters(cl, reverseIdMap)
		#print '!!!',list(infomap_clusters)
		#quit()
		#write_submission(i,list(infomap_clusters))
		#dendogram = g.community_edge_betweenness(False)
		#print dendogram
	
if __name__ == '__main__':
	main()
