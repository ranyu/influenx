def generate_node_features():
	features_name = ['user_id','my_view_ft','music_ft','color_ft','district_ft','language_ft',
	'age_ft','hobby_ft','education_finish_ft','movie_ft','interest_ft','book_ft','health_ft',
	'body_ft','science_ft','sport_ft','finish_percent_ft','computer_ft','concert_ft','subject_sport_ft',
	'goodnight_ft','favo_listen_music_ft','hobby_and_inserest_ft','relation_ft','friend_should_be_ft',
	'love_for_me_ft','hair_color_ft','alcohol_ft','zodiac_ft','eye_color_ft','pet_ft','journey_ft',
	'smoke_ft','find_what_ft','favor_movie_ft','politics_ft','car_ft','favo_music_ft','lifestyle_ft',
	'kitchen_ft','negative_sport_ft','child_relation','company_ft','food_ft','work_ft','sex_ft',
	'sex_relation_ft','marriage_ft','education_ft','public_ft','favor_movie_ft_2','art_ft','child_ft',
	'hair_type_ft','major_ft']
	node_features = {'user_id':[],'my_view_ft':[],'music_ft':[],'color_ft':[],'district_ft':[],
	'language_ft':[],'age_ft':[],'hobby_ft':[],'education_finish_ft':[],'movie_ft':[],'interest_ft':[],
	'book_ft':[],'health_ft':[],'body_ft':[],'science_ft':[],'sport_ft':[],'finish_percent_ft':[],
	'computer_ft':[],'concert_ft':[],'subject_sport_ft':[],'goodnight_ft':[],'favo_listen_music_ft':[],
	'hobby_and_inserest_ft':[],'relation_ft':[],'friend_should_be_ft':[],'love_for_me_ft':[],
	'hair_color_ft':[],'alcohol_ft':[],'zodiac_ft':[],'eye_color_ft':[],'pet_ft':[],'journey_ft':[],
	'smoke_ft':[],'find_what_ft':[],'favor_movie_ft':[],'politics_ft':[],'car_ft':[],'favo_music_ft':[],
	'lifestyle_ft':[],'kitchen_ft':[],'negative_sport_ft':[],'child_relation':[],'company_ft':[],'food_ft':[],
	'work_ft':[],'sex_ft':[],'sex_relation_ft':[],'marriage_ft':[],'education_ft':[],'public_ft':[],
	'favor_movie_ft_2':[],'art_ft':[],'child_ft':[],'hair_type_ft':[],'major_ft':[]}
	file_node = open('nodes.txt','w')
	with open('3.txt','r') as f:
		for data in f:
			node = data.strip().split()
			node_features[features_name[0]].append(node[0])
			i = 1
			for iters in xrange(1,len(features_name)):
				if str(iters) == node[i].split(':')[0]:					
					node_features[features_name[iters]].append(node[i].split(':')[1])
					i += 1
				else:
					node_features[features_name[iters]].append('0')
				if i == len(node):
					break
	'''for i in xrange(len(node_features)):
		file_node.write(features_name[i]+':')
		for j in xrange(len(node_features[features_name[i]])):
			file_node.write(node_features[features_name[i]][j]+',')
		file_node.write('\n')'''
def main():
	generate_node_features()
if __name__ == '__main__':
	main()