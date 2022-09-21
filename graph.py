import os
import pickle
from random import sample

# Saves an object as a pickle file; a compressed version
def save_as_pkl(object, path):
	pickle.dump(object, open(path, "wb"))

# Loads an object from a pickle file
def load_pkl(path):
	obj = pickle.load(open(path, "rb"))
	return obj

# Represents books as nodes in the graph
# with edges (neighbors) for each other book
# with common review words used
class Node:
	def __init__(self, name, neighbors):
		self.name = name
		self.neighbors = neighbors
	def get_neighbors(self):
		return self.neighbors

# Returns the top 10 most used words in reviews for each book
def find_top_10(top_items, excluded_list):
	top5 = {}
	for asin in top_items:
		top5[asin] = [[],[]]
		for word in top_items[asin]:
			if len(top5[asin][0]) < 5:
				if word not in excluded_list:
					top5[asin][0].append(word)
					top5[asin][1].append(top_items[asin][word])
			else:
				mi = min(top5[asin][1])
				if top_items[asin][word] > mi and word not in excluded_list:
					ind = top5[asin][1].index(mi)
					top5[asin][0][ind] = word
					top5[asin][1][ind] = top_items[asin][word]
	return top5

# Returns a dictionary of structure
# word:[list of asins whose reviews use that word], ...
def find_common_words(top5):
	common_words = {}
	for asin in top5:
		for word in top5[asin][0]:
			if word in common_words:
				common_words[word].append(asin)
			else:
				common_words[word] = [asin]
	return common_words

# Creates the adjacency list representation of the
# graph which is used for computing similar books
def make_graph(top5, common_words):
	graph = {}
	nodes = {}
	for asin in top5:
		neighbors = set([])
		for word in top5[asin][0]:
			neighbors = neighbors | set(common_words[word])
		nodes[asin] = Node(asin, neighbors)
		graph[asin] = neighbors
	return nodes

def create_samples(asin):
	# A list of words with no significance for
	# reader sentiment. These will be excluded from
	# common word comparisons between book reviews.
	excluded_list = ['this', 'the', 'a', 'i', 'and', 'to', 'of', 'in', 'my', 'is', 'with', 'that', 'it', 'as', 'be',
				'but', 'was', 'an', 'me', 'for', 'her', 'she', 'he', 'you', 'are', 'have', 'at', 'on', 'they',
				'also', 'almost', 'its', 'his', 'if', 'read', 'book', 'author', 'not', 'by', 'one', 'who',
				'what', 'from', 'too', 'or', 'there', 'did', 'so', 'us', 'all', 'we', 'out', 'will', 'just',
				'when', 'has', 'how', 'your', 'can', 'has', 'than', 'their', 'about', 'into', 'first',
				'story', 'books', 'ive', 'up', 'been', 'much', 'which', 'am', 'had', 'no', 'more', 'many',
				'do', 'our', 'get', 'like', 'very', 'characters', 'series', 'would', 'some', 'novel', 'really', 'other',
				'him', 'end', 'only', 'plot', 'even', 'stories', 'most', 'girl', 'put', 'still', 'after', 'man',
				'ending', 'two', 'them', 'people', 'reading', 'time', 'well', 'were', 'these', 'wait', 'because',
				'through', 'dont', 'down', 'didnt', 'cant', 'know', 'men', 'could', 'three']
	top_items = load_pkl('pickles/topItems.pkl')
	top5 = find_top_10(top_items, excluded_list)
	common_words = find_common_words(top5)
	graph = make_graph(top5, common_words)
	return sample(graph[asin].get_neighbors(), 10)
	