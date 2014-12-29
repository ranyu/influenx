import collections
import os
import igraph
from sets import Set

class Person(object):
    def __init__(self, personID ):
        self._personID = personID
        self._friends = set()
        self._features = {}
        
    def getFriends(self):
        return self._friends
    
    def getFeatures(self):
        return self._features
    
    def addFriend(self, friendID):
        return self._friends.add(friendID)
    
    def addFeature(self, key, value):
        self._features[key] = value
        
    def getFeature(self, key):
        return self._features.get(key, None)
    
    def isFriend(self, friendID):
        return (friendID in self._friends)
    
    
class Persons(object):
    def __init__(self):
        self._persons = {}
        self._originalPersons = []
        
    def getPerson(self, person_ID):
        if person_ID not in self._persons:
            self._persons[person_ID] = Person(person_ID)
        
        return self._persons[person_ID]
    
    def getAllPersons(self):
        return self._persons
        
    def addOriginalPerson(self, originalPersonID):
        self._originalPersons.append(originalPersonID)
        
    def getOriginalPersons(self):
        return self._originalPersons
    
class Data:
    def __init__(self):
        self.friendMap = None
        self.originalPeople = None
        self.featureMap = None
        self.featureList = None
        self.trainingMap = None
        self.persons = Persons()

def loadEgoNets(directory):
    friendMap = collections.defaultdict(set)
    originalPeople = []
    persons = Persons()
    
    for egonetFile in os.listdir(directory):

        currentPerson = egonetFile[:egonetFile.find('.')]
        originalPeople.append(currentPerson)
        persons.addOriginalPerson(currentPerson)
               
        egonetFilePath = os.path.join(directory, egonetFile)

        for line in open(egonetFilePath):
            line = line.strip().split(':')
            currentFriend = line[0]

            friendMap[currentPerson].add(currentFriend)
            friendMap[currentFriend].add(currentPerson)
            persons.getPerson(currentPerson).addFriend(currentFriend)
            persons.getPerson(currentFriend).addFriend(currentPerson)
            
            friends = line[1].strip().split()

            for friend in friends:
                friendMap[currentFriend].add(friend)
                friendMap[friend].add(currentFriend)
                persons.getPerson(currentFriend).addFriend(friend)
                persons.getPerson(friend).addFriend(currentFriend)
            
                friendMap[currentPerson].add(friend)
                friendMap[friend].add(currentPerson)
                persons.getPerson(currentPerson).addFriend(friend)
                persons.getPerson(friend).addFriend(currentPerson)
            
    return friendMap, originalPeople, persons
def loadFeatures(filename, persons = None):
    featureMap = collections.defaultdict(dict)
    for line in open(filename):
        parts = line.strip().split()
        currentPerson = parts[0]
        for part in parts[1:]:
            key = part[0:part.rfind(';')]
            value = part[part.rfind(';')+1:]
            featureMap[currentPerson][key] = value
            if persons != None:
                persons.getPerson(currentPerson).addFeature(key, value)
    return featureMap

def loadFeatureList(filename, featureweight_filename):
    featureList = []
    feature_Wlist = {}
    for line in open(filename):
        featureList.append(line.strip())
    for line in open(featureweight_filename):
        line = line.strip()
        weight = line.split("--")
        feature_Wlist[weight[0]] = float(weight[1])
    return featureList, feature_Wlist
def loadTrainingData(directory):
    trainingMap = collections.defaultdict(list)

    for trainingFile in os.listdir(directory):
        currentPerson = trainingFile[:trainingFile.find('.')]

        trainingFilePath = os.path.join(directory, trainingFile)
        for line in open(trainingFilePath):
            parts = line.strip().split()
            trainingMap[currentPerson].append(parts[1:])

    return trainingMap

def name(sourceName, targetName):
    if sourceName < targetName:
        return str(sourceName) + '-' + str(targetName)
    else:
        return str(targetName) + '-' + str(sourceName)

def extract_clusters(clusters, reverseIdMap):
    new_clusters = []
    for i in range(len(clusters)):
        next_cluster = [reverseIdMap[j] for j in clusters[i]]
        new_clusters.append(next_cluster)
    return new_clusters

def writeSubmission(filename, circleMap, test=False):
    f = open(filename, 'w+')

    f.write('UserId,Predicted\n')

    for person, circles in circleMap.iteritems():

        line = person + ','

        if not test:
            for i in range(len(circles)):#circle in circles:
                for j in range(len(circles[i])):#friend in circles[i]:
                    line += circles[i][j]
                    if j != len(circles[i]) - 1:
                        line += ' '
                if i != len(circles) - 1:
                    line += ';'
        else:
            for friend in circles:
                line += friend + ' '
            line += ';'


        line += '\n'
        f.write(line)

    f.close()


def community_using_igraph(data, origPerson):
    friendMap = data.friendMap
    # We will map ids to indices in the Graph.
    idMap = {}
    reverseIdMap = {}

    added_edges = Set()

    numFriends = len(friendMap[origPerson])
    idMap[origPerson] = numFriends - 1

    # Create person to index mappings
    currentId = 0
    for friend in friendMap[origPerson]:
        idMap[friend] = currentId
        reverseIdMap[currentId] = friend
        currentId += 1

    g = igraph.Graph()
    #g.es['weight'] = 1.0

    g.add_vertices(numFriends)

    for source in idMap:
        for target in idMap:
            # Do not add self edges
            if source != target:
                sourceName = idMap[source]
                targetName = idMap[target]
                edgeName = name(sourceName, targetName)
                # Do not add the same edge twice
                #weight = edgeFunc(data, source, target)
                if not edgeName in added_edges:
                    g.add_edge(sourceName, targetName)
                    added_edges.add(edgeName)
                    #g[sourceName, targetName] = weight
    print g
    quit()
    '''vd_betweenness = g.community_edge_betweenness(directed=False)
    print vd_betweenness#.as_clustering(5)'''

    #raw_input()

    # vd_betweenness = g.community_edge_betweenness(directed=False)
    #TODO print vd_betweenness#.as_clustering(5)

    # vd_fastgreedy = g.community_fastgreedy()
    #TODO print vd_fastgreedy

    try:
        # edge_weights, vertex_weights
        clusters = g.community_infomap(edge_weights='weight')        
    except:
        clusters = []
    infomap_clusters = extract_clusters(clusters, reverseIdMap)
    #infomap_clusters = pruneFunc(data, origPerson, infomap_clusters)

    """
    try:
        # weights
        #clusters = g.community_leading_eigenvector(weights='weight')
        None
    except:
        clusters = []
    eigen_clusters = extract_clusters(clusters, reverseIdMap)

    try:
        # weights
        #clusters = g.community_label_propagation(weights='weights')
        None
    except:
        clusters = []
    label_clusters = extract_clusters(clusters, reverseIdMap)

    try:
        # weights
        #clusters = g.community_multilevel(weights='weight')
        None
    except:
        clusters = []
    multi_clusters = extract_clusters(clusters, reverseIdMap)

    try:
        None
        #clusters = g.community_spinglass(weights='weight')
    except:
        clusters = []
    spin_clusters = extract_clusters(clusters, reverseIdMap)

    #TODO print g.community_walktrap()

    return infomap_clusters, eigen_clusters, label_clusters, multi_clusters, spin_clusters
    """
    return infomap_clusters

def main():
	# Input data locations.
    EGONET_DIR = 'egonets'
    TRAINING_DIR = 'Training'
    FEATURE_FILE = 'features.txt'
    FEATURE_LIST_FILE = 'featureList.txt'
    FEATURE_WEIGHT_FILE = "feature_weights.txt"

    print 'Loading input data.'
    data = Data()

    # Load friend map.
    data.friendMap, data.originalPeople, data.persons = loadEgoNets(EGONET_DIR)
    
    # Load features.
    data.featureMap = loadFeatures(FEATURE_FILE, data.persons)

    # Load feature list
    data.featureList, featureWeightMap = loadFeatureList(FEATURE_LIST_FILE,FEATURE_WEIGHT_FILE)

    # Load training data.
    data.trainingMap = loadTrainingData(TRAINING_DIR)

    # List of people to calculate training data for.
    trainingPeople = []
    for key in data.trainingMap:
        trainingPeople.append(key)
    print trainingPeople
    kagglePeople = [origPerson for origPerson in data.originalPeople if origPerson
            not in trainingPeople]
    print kagglePeople
    #print data.friendMap
    print 'Calculating Kaggle submission data.'

    # Reset dictionaries.
    info_clusters_dict = {}
    eigen_clusters_dict = {}
    label_clusters_dict = {}
    multi_clusters_dict = {}
    spin_clusters_dict = {}

    for origPersonIndex in range(len(kagglePeople)):
        print '\t' + str(1 + origPersonIndex) + '/' + str(len(kagglePeople))
        origPerson = kagglePeople[origPersonIndex]
        info_clusters = community_using_igraph(data, origPerson)

        info_clusters_dict[origPerson] = info_clusters

    info_clusters_data = 'kaggle_infomap_clusters_data.csv'

    writeSubmission(info_clusters_data, info_clusters_dict)

    print 'Kaggle submission data:'
    print '\t', info_clusters_data
if __name__ == '__main__':
	main()