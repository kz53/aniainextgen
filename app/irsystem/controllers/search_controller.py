from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import numpy as np
import json
import operator
import gensim.models
import re

project_name = "AniAi: Anime Recommender"
net_id = "Arthur Chen (ac2266), Henry Levine (hal59), Kelley Zhang (kz53), Gary Gao (gg392), Cheyenne Biolsi (ckb59)"
# animelite.csv
animelite = json.load(open('data/animelite.json'))

synposis_tfidf = np.load('data/synposis_tfidf.npy')
tsynposis = synposis_tfidf
# u, s, vh = np.linalg.svd(synposis_tfidf, full_matrices=True)

tags_data = np.load('data/tags.npy')
firstcolumn = synposis_tfidf[:,0]

# dov2vec
review_model = gensim.models.doc2vec.Doc2Vec.load("data/doc2vecreview.model")
synopsis_model = gensim.models.doc2vec.Doc2Vec.load("data/doc2vecsynopsis.model")

# truncated svd


tags_array = ['action','adventure','cars','comedy','dementia','demons','mystery','drama','ecchi','fantasy','game','hentai','historical','horror','kids','magic','martial_arts','mecha','music','parody','samurai','romance','school','sci-fi','shoujo','shoujo_ai','shounen','shounen_ai','space','sports','super_power','vampire','yaoi','yuri','harem','slice_of_life','supernatural','military','police','psychological','thriller','seinen','josei']
tags_set = set(tags_array)

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	tag = request.args.get('tagsearch')
	hide_ss = request.args.get('hide_ss')
	tv = request.args.get('TV')
	movie = request.args.get('movie')
	ova = request.args.get('ova')
	ona = request.args.get('ona')
	special = request.args.get('special')

	show = []
	if tv:
		show.append('TV')

	if movie:
		show.append('Movie')

	if ova:
		show.append('OVA')

	if ona:
		show.append('ONA')

	if special:
		show.append('Special')

	print('Show', show)


	min_rating = request.args.get('min_rating')
	# print('minimum', min_rating)
	time = request.args.get('time')
	finished = request.args.get('finished')
	licensed = request.args.get('licensed')

	if not query and not tag:
		data = []
		output_message = ''

	elif not query and tag: # Need Still Work
		tag_array = tag.split('|')
		tag_indexes = []
		for tag_input in tag_array:
			tag_index = -1
			for element in tags_set:
				if element == tag_input:
					tag_index = tags_array.index(tag_input)
			tag_indexes.append(tag_index)

		if -1 in tag_indexes:
			data = []
			output_message = 'Tag(s) ' + tag + ' do not exist. Pls try again.'
		else:
			output_message = 'You looked for the Tag(s) ' + tag
			mytag = []
			for tag_input in tag_indexes:
				mytag.append(tag_input)
			mytag_set = set(mytag)

			jaccsim_matrix = np.zeros(firstcolumn.size)
			for i in range(firstcolumn.size-1):
				anime_i_tags = np.where(tags_data[i,:] > 0)[0]
				anime_i_set = set(anime_i_tags)
				jaccsim_matrix[i] = get_jaccard(mytag_set, anime_i_set)

			jaccard_order = np.argpartition(jaccsim_matrix, -10)[-10:]
			data = []
			for ind in jaccard_order:
				data.append(animelite[ind])

	elif not tag and query:
		
		query_array = query.split('|')
		anime_indexes = []
		for anime_input in query_array:
			anime_index = -1
			for element in animelite:
				if element['anime_english_title'] == anime_input:
					anime_index = element['anime_id']
			anime_indexes.append(anime_index)
			 
		set_anime_ids = set(anime_indexes)

		if -1 in anime_indexes:
			data = []
			output_message = 'Could not find ' + query + '. Please try again pls.'
		else:
			output_message = 'Your search: ' + query


			# ## DOC2VEC
			positive = []
			for ind in anime_indexes:
				positive.append("anime_id_" + str(ind))

			positive_vectors = []
			for anime_id in positive:
				reviewvector = review_model.docvecs[anime_id] #get vector by MAL id
				positive_vectors.append(reviewvector)

			most_similar = review_model.docvecs.most_similar(positive=positive_vectors, negative=[], topn=200) #returns most similar anime ids and similarity scores
			top10 = most_similar
			# print(np.array(top10).shape)

			json_array = []
			# get_anime(anime_id, animelite):
			for result in top10:
				# print(result[0].replace("anime_id_", ""))
				get_anime_id = int(result[0].replace("anime_id_", ""))
				# print(get_anime_id)
				# if get_anime_id not in set_anime_ids:
				jsonfile = get_anime(get_anime_id, animelite)
				if get_anime_id not in set_anime_ids and jsonfile != "not found":
					json_array.append(jsonfile)

			data = json_array

			if hide_ss:
				data = hide(anime_indexes, data, animelite)

			data = hide2(data, animelite, show, min_rating, time, finished, licensed)
			
			# hide2(data, jsonfile, show, min_rating, time, finished, licensed):

			# Trucated SVD
			# query_vector = np.zeros(synposis_tfidf.shape[1])
			# for ind in anime_indexes:
			# 	column_index = np.where(firstcolumn == ind)[0][0]
			# 	query_vector += synposis_tfidf[column_index]
			
			# cossim = {}
			# for i in range(firstcolumn.size):
			# 	cossim[i] = get_cossim(query_vector, i, synposis_tfidf)
			# top10results = dict(sorted(cossim.items(), key=lambda x: x[1], reverse=True)[:11])
			# top10results_list = top10results.keys()[1:] #these are column indexes, we need anime ids
			# top10animes = firstcolumn[top10results_list]

			# json_array = []
			# for result in top10animes:
			# 	json_array.append(get_anime(result, animelite))

			# data = json_array

	else: # Tag and Anime Still Needs Work

		output_message = "Your search: " + query + ' ' + 'tags ' + tag

		query_array = query.split('|')
		anime_indexes = []
		for anime_input in query_array:
			anime_index = -1
			for element in animelite:
				if element['anime_english_title'] == anime_input:
					anime_index = element['anime_id']
			anime_indexes.append(anime_index)

		tag_array = tag.split('|')
		tag_indexes = []
		for tag_input in tag_array:
			tag_index = -1
			for element in tags_set:
				if element == tag_input:
					tag_index = tags_array.index(tag_input)
			tag_indexes.append(tag_index)


		if (-1 in tag_indexes) and (-1 in anime_indexes):
			data = []
			output_message = 'Wrong Tag(s) and Anime.'

		elif -1 in anime_indexes:
			data = []
			output_message = 'Wrong Anime'
		
		elif -1 in tag_indexes:
			data = []
			output_message = 'Tag(s) ' + tag + ' do not exist. Pls try again.'
	
		else:
			query_vector = np.zeros(synposis_tfidf.shape[1])
			for ind in anime_indexes:
				column_index = np.where(firstcolumn == ind)[0][0]
				query_vector += synposis_tfidf[column_index]

			cossim = {}
			for i in range(firstcolumn.size):
				cossim[i] = get_cossim(query_vector, i, synposis_tfidf)

			topresults = dict(sorted(cossim.items(), key=lambda x: x[1], reverse=True)[:11])
			topresults_list = topresults.keys()[1:] #these are column indexes, we need anime ids
			# topanimes = firstcolumn[topresults_list] #these are anime ids

			mytag = []
			for tag_input in tag_indexes:
				mytag.append(tag_input)
			mytag_set = set(mytag)

			# jaccsim_matrix = np.zeros(np.array(topresults_list).size)
			jaccsim_matrix = []
			for i in topresults_list:
				anime_i_tags = np.where(tags_data[i,:] > 0)[0]
				anime_i_set = set(anime_i_tags)
				jaccsim_matrix.append(get_jaccard(mytag_set, anime_i_set))

			jaccard_order = np.argpartition(jaccsim_matrix, -10)[-10:]
			data = []
			for ind in jaccard_order:
				data.append(animelite[topresults_list[ind]]) # need column ids

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

def get_anime(anime_id, jsonfile):
	# print(anime_id)
	for element in jsonfile:
		# print(element['anime_id'])
		if element['anime_id'] == anime_id:
			return element
	return "not found"

def get_sim(index, ind2, tfidf):
    """Returns a float giving the cosine similarity of 
       the two movie transcripts.
    
    Params: {mov1: String,
             mov2: String,
             input_doc_mat: Numpy Array,
             movie_name_to_index: Dict}
    Returns: Float (Cosine similarity of the two movie transcripts.)
    """
    # YOUR CODE HERE
    # numpy matrix whose shape is the number of documents by the number of words you're considering max 5000
    queryvector = tfidf[index,:]
    othervector = tfidf[ind2,:]
    numerator = np.dot(queryvector, othervector)
    denominator = (np.dot(np.linalg.norm(queryvector), np.linalg.norm(othervector)))
    return numerator/denominator

def get_cossim(queryvector, ind2, tfidf):
    """Returns a float giving the cosine similarity of 
       the two movie transcripts.
    
    Params: {mov1: String,
             mov2: String,
             input_doc_mat: Numpy Array,
             movie_name_to_index: Dict}
    Returns: Float (Cosine similarity of the two movie transcripts.)
    """
    # YOUR CODE HERE
    # numpy matrix whose shape is the number of documents by the number of words you're considering max 5000
    othervector = tfidf[ind2,:]
    numerator = np.dot(queryvector, othervector)
    denominator = (np.dot(np.linalg.norm(queryvector), np.linalg.norm(othervector)))
    return numerator/denominator

def get_jaccard(setA, setB):
	jacsim = len(setA & setB)/len(setA | setB) 
	return jacsim

def hide(anime_ids, data, jsonfile):

	#hide
	hide = []
	for anime_id in anime_ids:
		anime = get_anime(anime_id, jsonfile)
		sidestory = anime["anime_side_story"]
		sidestory_anime = re.findall('\((.*?)\)',sidestory)
		for ss in sidestory_anime:
			hide.append(int(ss.replace('anime ','')))
	hide_set = set(hide)
	new_data = []

	for entry in data:
		if entry != "not found":
			if entry['anime_id'] not in hide_set:
				new_data.append(entry)

	return new_data
		

def hide2(data, jsonfile, show, min_rating, time, finished, licensed):
	# Filters: TV, Movie, OVA, Special, OVA, Minimum Anime Rating, Time Period
	new_data = []
	for entry in data:
		if entry != "not found":

			min_rating_add = True
			# print('wtf2', min_rating)
			if min_rating: 
				if entry['anime_rating_value'] != "":
					# print('wtf', float(entry['anime_rating_value']))
					# print('help',entry['anime_rating_value'] < min_rating)
					# print(entry['anime_rating_value'])
					if float(entry['anime_rating_value']) < float(min_rating):
						min_rating_add = False
				else:
					min_rating_add = False
			# Fixed

			time_add = True
			if time:
				if entry['anime_premiered'] != 'N/A':
					year = re.findall('\d', entry['anime_premiered'])
					year = ''.join(year)
					# print(re.findall('\d',entry['anime_premiered'])[0:4])
					# print(year)
					if year < int(time):
						time_add = False
				else:
					time_add = False
			# Fixed			

			finished_add = True
			if finished:
				if entry['anime_status'] != "Finished Airing" and entry['anime_status'] != "":
					finished_add = False

			# Fixed

			
			show_set = set(show)
			# print(show_set)
			show_add = True
			if show:
				# print('show', entry['anime_type'])
				# print(entry['anime_type'] not in show_set)
				if entry['anime_type'] not in show_set:
					# TV, Movie, OVA, Special, OVA 
					show_add = False

			# Fixed

			licensed_add = True
			if licensed:
				if entry['anime_licensors'] == "":
					licensed_add = False

			# Fixed

			if min_rating_add and time_add and finished_add and show_add and licensed_add:
				new_data.append(entry)


	return new_data





