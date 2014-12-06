import csv
import re
from operator import itemgetter

def generate_data():
	file = open('pre_nodes_profile.csv','rb')
	#file2 = open('2.txt','w')
	file_feature = open('only_region.txt','w')
	file.readline()
	max_features_num_column = {}
	column = {}
	for i in xrange(1,55):
		max_features_num_column[i] = 0
	column_elelment = {}
	reader = csv.reader(file)
	for item in reader:
		column[item[0]] = {}		
		for i in xrange(1,len(item)):
			number_column = 0
			column_elelment = re.findall(r'[\d|.]+',item[i])
			if len(column_elelment) != 0:
				column[item[0]][i] = list()
				column[item[0]][i] = column_elelment
				'''for s in xrange(len(column[item[0]][str(i)])):
					file2.write(item[0]+' '+str(i)+' '+str(s)+' '+column[item[0]][str(i)][s]+' ')
				file2.write('\n')'''	
			for k in xrange(len(column_elelment)):		
				number_column = int(column_elelment[k])
				if max_features_num_column[i] < number_column:
					max_features_num_column[i] = number_column
	print max_features_num_column
	length_of_column = len(item)
	features = {}
	feature_element = {}
	for i in column.keys():
		index = 0	
		column_keys = {}
		features[i] = {}
		for l in xrange(len(column[i].keys())):
			column_keys[l] = int(column[i].keys()[l])
		pp = sorted(column_keys.iteritems(), key=itemgetter(1))
		j_keys = []
		for j in pp:
			j_keys.append(j[1])
		for num in xrange(1,length_of_column):
			if num in j_keys:
				features[i][num] = dict()
				for k in column[i][num]:
					if len(column[i][num]) == 1:
						features[i][num].setdefault(int(k)+index,column[i][num][0])
					else:
						features[i][num].setdefault(int(k)+index,'1')
			index += max_features_num_column[num]
	for i in column.keys():
		file_feature.write(i + ' ')
		for j in features[i]:
			for k in features[i][j]:
				file_feature.write(str(k)+':'+features[i][j][k]+' ')
		file_feature.write('\n')
	file.close()
	file_feature.close()
def change_data2_index(data2,length):
	del data2[0]
        for i in xrange(0,len(data2)):
		modifier = str(length+int(data2[i].split(':')[0]))	# modify the index
		data2[i] = modifier+':'+data2[i].split(':')[1]
	print data2
	raw_input()
	return data2
def generate_edge_feature(number_of_lines,max_index_length):
	file_edges = open('edges.txt','w')
        times = 1
	with open('3.txt','r') as file_nodes:
		for i in xrange(number_of_lines):
			data1 = file_nodes.readline().strip().split()			
			#print data1
                        for j in xrange(number_of_lines-1):
				memo = data1[:]
				data2 = file_nodes.readline().strip().split()
				data1.insert(1,data2[0])
                                #
				data2 = change_data2_index(data2,max_index_length)
				#
				data1.extend(data2)
				print data1
				raw_input()
				for k in xrange(len(data1)):
					file_edges.write(data1[k]+' ')
				file_edges.write('\n')
                                data1 = memo[:]	
				#quit()
				#file_edges.write(data1 + data2)
			        #print data1,data2
                                #raw_input()
			
			file_nodes.seek(0,0)
                        #print i
                        for x in xrange(i):
			    file_nodes.readline() 
                        #raw_input()
                        #print file_nodes.readline().strip().split()
			raw_input()
                        #quit()
		#quit()
	#data_2 = file_nodes.readline().strip().split()
	file_edges.close()
def main():
	#generate_data()
	generate_edge_feature(100056,93220)
if __name__ == '__main__':
	main()
