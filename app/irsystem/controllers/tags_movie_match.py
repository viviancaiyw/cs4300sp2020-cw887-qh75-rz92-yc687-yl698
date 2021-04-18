import json
import re
import itertools
from collections import Counter
import numpy as np
import time

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn


lemmatizer = WordNetLemmatizer()
tag_stop_words = ['game', 'play', 'video', 'steam']



# Cleaning

'''
Clean a string by lowercasing and removing punctuations.
'''
def _clean_str(string):
	string = string.lower()
	string = re.sub('[^A-Za-z]+', ' ', string).strip()
	return string


'''
Clean a synonym.
'''
def _clean_syn(syn):
	cleaned = _clean_str(syn)

	# Filter synonym with punctuations
	if cleaned != syn:
		return []

	# Filter synonym with more than 1 word
	split = cleaned.split(' ')
	split = list(filter(lambda x: len(x)>2, split))
	return split

'''
Clean a list of synonyms.
'''
def _clean_syns(syns):
	syns = list(map(_clean_syn, syns))
	syns = list(itertools.chain(*syns))
	return syns


'''
Clean a tag.
'''
def _clean_tag(tag):
	tag = _clean_str(tag)

	# Lemmatize tag with a single word
	if len(tag.split(' '))==1:
		(tag,pos) = nltk.pos_tag([tag])[0]
		if pos != 'n' and pos != 'a':
			pos = 'n'
		tag = lemmatizer.lemmatize(tag, pos)

	return tag


'''
Clean a lis tof tags.
'''
def _clean_tags(tags):
	tags = list(map(_clean_tag, tags))

	# Filter tags that are stopwords.
	tags = list(filter(lambda x: x not in tag_stop_words, tags))
	return tags





# Keyword match
'''
Get word to tag dict.
'''
def _get_word_to_tags(tags):
	word_to_tags = dict()
	for tag in tags:
		for word in tag.split(' '):
			lst = word_to_tags.get(word, list())
			lst.append(tag)
			word_to_tags[word] = lst
	return word_to_tags


'''
Get a list of synonyms for the given word.
'''
def _get_syns(word):
	syns = set()

	# Get all the synonyms for the word when the word is a noun / adj.
	synsets = wn.synsets(word, pos=wn.NOUN)
	synsets.extend(wn.synsets(word, pos=wn.ADJ))

	for sense in synsets:
		if sense.pos()=='s':
			sense = sense.similar_tos()[0]
		syns.update(_clean_syns(sense.lemma_names()))

	if word in syns:
		syns.remove(word)
	return list(syns)

'''
Get a list of derived adjs for the given word if the word is a noun.
'''
def _get_derived(word, pos):
	derived = set()

	synsets = wn.synsets(word, pos=pos)

	# Only get derived words for a noun.
	if pos=='n':
		for sense in synsets:
			curr_derived = [n.name() for l in sense.lemmas() \
								for n in l.derivationally_related_forms()]
			curr_derived = _clean_syns(curr_derived)

			# Only keep derived words that are adj.
			curr_derived = list(filter(
				lambda x: nltk.pos_tag([x])[0][1][:2]=='JJ', curr_derived))
			derived.update(curr_derived)
	return list(derived)



'''
Get a word_vector representation for the tags that are split to words to use 
for keyword matching with games.

return: (word_vector, norm, addedword_to_originalwords)
'''
def _get_keyword_match_wordvector(tag_words, common_keywords_keyphrases, addedword_to_originalwords):

	# Get syns for each word in tags.
	# Get all the words to put in the final vector.
	# This includes words appear in the tags and their synonyms.
	allwords = list(tag_words)
	for word in set(tag_words):
		syns = _get_syns(word)
		allwords.extend(syns)

		for syn in syns:
			lst = addedword_to_originalwords.get(syn, list())
			lst.append(word)
			addedword_to_originalwords[syn] = lst

	# Calculate weights for each word.

	# Start by counting word frequency.
	weight = dict(Counter(allwords))

	# Adjust weight based on word pos 
	# and whether it's the original word given by the user
	for word in set(tag_words):
		(word,pos) = nltk.pos_tag([word])[0]

		# If it's an extracted common keyword, put more weight.
		if word in common_keywords_keyphrases:
			weight[word] = weight[word]*6

		if pos[:2]=='NN':
			if word in tag_words:
				weight[word] = weight[word]*2
			else:
				weight[word] = weight[word]*1.75
			pos = 'n'
		elif pos[:2]=='JJ':
			if word in tag_words:
				weight[word] = weight[word]*1.75
			else:
				weight[word] = weight[word]*1.5
			pos = 'a'
		else:
			continue


	# Adjust weight for derived words.
	derived = _get_derived(word, pos)

	for dv in derived:
		if dv not in weight.keys():
			weight[dv] = weight[word]*0.9

		lst = addedword_to_originalwords.get(dv, list())
		lst.append(dv)
		addedword_to_originalwords[dv] = lst

	vector = np.array(list(weight.values()))
	squared = vector ** 2
	norm = np.sum(squared)
	norm = np.sqrt(norm)

	return weight, norm, addedword_to_originalwords

'''
Compute cosine similarity between two dictionaries.
'''
def _cos_sim(d1, d2, norm1, norm2):
	intersect = set(d1.keys()).intersection(set(d2.keys()))
	score = sum(d1[k]*d2[k] for k in intersect)
	return (score, intersect)

'''
Get the original words from the added words.

return: set of original words
'''
def _change_addedword_to_originalword(intersect, addedword_to_originalwords):
	res = set()
	for word in intersect:
		res.update(addedword_to_originalwords.get(word, list()))
	return res


'''
Get keyword match results.

return: ranked [(app_id, (score, word_matchs))]
'''
def _match_games_using_keywords(tags, appid_to_vec, common_keywords_keyphrases):

	def _get_sim_res(d1, d2, norm1, norm2, addedword_to_originalwords):
		(score, intersect) = _cos_sim(d1, d2, norm1, norm2)
		intersect = _change_addedword_to_originalword(intersect, addedword_to_originalwords)
		return (score, intersect)


	tag_words = list(map(lambda x: x.split(' '), tags))
	tag_words = list(itertools.chain(*tag_words))

	words_only = set(filter(lambda x: len(x.split(' '))==1, tags))

	addedword_to_originalwords = {word:[word] for word in words_only}
	vector, norm, addedword_to_originalwords = _get_keyword_match_wordvector(tag_words, common_keywords_keyphrases, addedword_to_originalwords)

	addedword_to_originalwords_keys = list(addedword_to_originalwords.keys())
	for word in addedword_to_originalwords_keys:
		if word not in words_only:
			addedword_to_originalwords.pop(word)

	res = list(map(lambda x: 
						(x['app_id'], _get_sim_res(vector, x['vector'], norm, x['norm'], addedword_to_originalwords)), 
					appid_to_vec.values()))
	res = list(filter(lambda x: x[1][0]!=0, res))
	res = sorted(res, key=lambda x:(-x[1][0], -len(x[1][1]), x[0]))

	return res




# Keyphrase match

'''
Get keyphrase match results.

return: ranked [(app_id, (score, phrase_matchs))]
'''
def _match_games_using_keyphrases(tags, appid_to_vec, common_keywords_keyphrases, word_to_synphrases, inv_keywords_phrases):
	weight = dict()

	word_to_tags = _get_word_to_tags(tags)

	words = list(word_to_tags.keys())
	phrases = [x for x in tags if x not in words]


	# If the given keyphrase is a common keyphrase, add weight.
	for phrase in phrases:
		if phrase in common_keywords_keyphrases['keyphrases']:
			weight[phrase] = 6

	for word in words:
		(word, pos) = nltk.pos_tag([word])[0]
		# Only get synphrases if the word is a noun.
		if pos=='n':
			synphrases = word_to_synphrases.get(word, list())
			for synphrase in synphrases:
				weight[word_to_tags[word]] = 1.75

	game_to_score = dict()
	game_to_phrases = dict()
	for tag in weight.keys():
		games = inv_keywords_phrases.get(tag, list())

		for game in games:
			score = game_to_score.get(game, 0)
			score += weight[tag]
			phrases = game_to_phrases.get(game, set())
			phrases.add(tag)

			game_to_score[game] = score
			game_to_phrases[game] = phrases

	res = [(game, (game_to_score[game], game_to_phrases[game])) for game in game_to_score.keys()]
	res = sorted(res, key=lambda x:(-x[1][0], -len(x[1][1]), x[0]))
	return res

'''
Merge keyword match results and keyphrase match results.

return [(app_id, tag_matchs)] in ranking order.
'''
def _merge_keyword_keyphrase_match_results(keyword_matchs, keyphrase_matchs):
	# Assign new score.
	num_keyword_matches = len(keyword_matchs)

	res = dict()

	rank = 0
	last_old_score = 0
	for match in keyword_matchs:
		app_id = match[0]
		old_score = match[1][0]

		if last_old_score != old_score:
			rank+=1

		new_score = num_keyword_matches - rank
		
		res[app_id] = (new_score, match[1][1])

	for match in keyphrase_matchs:
		app_id = match[0]

		(score, tag_matchs) = res.get(app_id, (0, set()))
		score += match[1][0]
		tag_matchs.update(match[1][1])
		tag_matchs = set(tag_matchs)

		res[app_id] = (score, tag_matchs)

	res = list(filter(lambda x: len(x[1][1])!=0, res.items()))
	res = sorted(res, key=lambda x: (-len(x[1][1]), -x[1][0], x[0]))
	res = [(k, list(v[1])) for (k,v) in res]

	return res

'''
Merge results from matching input tags and results from matching movie.

return: [{
			'app_id': app_id, 
			'score': score, 
			'tags_match': [tag1, tag2, ...],
			'num_movie_keyword_match': num_movie_keyword_match,
			'tags_rank': rank in tags_match results,
			'movie_rank': rank in movie_match results
		}]
'''

def _merge_two_results(tags_match, movie_match, tags_weight, movie_weight):
	len_tags_match = len(tags_match)
	len_movie_match = len(movie_match)

	tags_d = dict()
	for i in range(len_tags_match):
		tags_d[tags_match[i][0]] = (i, tags_match[i][1])
	movie_d = dict()
	for i in range(len_movie_match):
		movie_d[movie_match[i][0]] = (i, movie_match[i][1])


	def _compute_score_for_one_game(app_id):
		if app_id in tags_d:
			tags_rank = tags_d[app_id][0]
		else:
			tags_rank = len_tags_match

		if app_id in movie_d:
			movie_rank = movie_d[app_id][0]
		else:
			movie_rank = len_movie_match

		tags_score = (1-tags_rank/len_tags_match) * len(tags_d[app_id][1])
		movie_score = (1-movie_rank/len_movie_match)
		score = tags_weight*tags_score + movie_weight*movie_score
		return score

	allgames = set(tags_d.keys()).intersection(set(movie_d.keys()))
	res = [
			{'app_id':app_id, 'score':_compute_score_for_one_game(app_id),\
	  		'tags_match': tags_d[app_id][1], 'num_movie_keyword_match': len(movie_d[app_id][1]),
	  		'tags_rank': tags_d[app_id][0], 'movie_rank': movie_d[app_id][0]}
	  		for app_id in allgames]
	res = sorted(res, key=lambda x: (-x['score'], -len(x['tags_match']), -x['num_movie_keyword_match']))

	return res





'''
Get tags and movie keyword match results.

return [(app_id, (score, tag_matchs))]
'''
def match_tags_and_movie(input_tags, movielink):

	# TODO: remove
	path = '/Users/viviancai/Desktop/cs4300/cs4300sp2021-cw887-qh75-rz92-yc687-yl698/data/reviews/'
	
	with open(path+'keyphrases_and_keywords.json', 'r', encoding='utf8') as in_json_file:
		common_keywords_keyphrases = json.load(in_json_file)

	with open(path+'appid_to_vec.json', 'r', encoding='utf8') as in_json_file:
		appid_to_vec = json.load(in_json_file)

	# with open(path+'movielink_to_vec.json', 'r', encoding='utf8') as in_json_file:
		# movielink_to_vec = json.load(in_json_file)

	with open(path+'phrase_word_to_synphrase.json', 'r', encoding='utf8') as in_json_file:
		word_to_synphrases = json.load(in_json_file)

	with open(path+'inverse_keyword_phrases.json', 'r', encoding='utf8') as in_json_file:
		inv_keywords_phrases = json.load(in_json_file)

	start = time.time()
	tags = _clean_tags(input_tags)

	# Match with tags
	keyword_matchs = _match_games_using_keywords(tags, appid_to_vec, common_keywords_keyphrases)
	keyphrase_matchs = _match_games_using_keyphrases(tags, appid_to_vec, common_keywords_keyphrases, word_to_synphrases, inv_keywords_phrases)

	res = _merge_keyword_keyphrase_match_results(keyword_matchs, keyphrase_matchs)


	# Now match with movie
	with open(path+'movie_info/info_'+movielink+'.json', 'r', encoding='utf8') as in_json_file:
		movie_info = json.load(in_json_file)

	movie_tags = [word for word in movie_info['keywords']]
	movie_tags.extend([phrase for phrase in movie_info['keyphrases']])
	filtered_appids = [x[0] for x in res]
	filtered_appid_to_vec = dict(filter(lambda x: x[1]['app_id'] in filtered_appids, appid_to_vec.items()))


	movie_keyword_matchs = _match_games_using_keywords(movie_tags, filtered_appid_to_vec, common_keywords_keyphrases)
	movie_keyphrase_matchs = _match_games_using_keyphrases(movie_tags, filtered_appid_to_vec, common_keywords_keyphrases, word_to_synphrases, inv_keywords_phrases)

	movie_res = _merge_keyword_keyphrase_match_results(movie_keyword_matchs, movie_keyphrase_matchs)

	combined = _merge_two_results(res, movie_res, 0.9, 0.1)
	print(time.time()-start)

	return combined[:20]






# TODO: remove
if __name__ == "__main__":

	input_tags = ['game', 'geralt', 'open world']
	movielink = 'the_witch_2016'

	res = match_tags_and_movie(input_tags, movielink)

	# print(res[:20])





