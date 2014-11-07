import csv
import re
from operator import itemgetter

def generate_data():
	file = open('pre_nodes_profile.csv','rb')
	#file2 = open('2.txt','w')
	file_feature = open('3.txt','w')
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
def main():
	generate_data()
if __name__ == '__main__':
	main()