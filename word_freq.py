from json_sampler import load_pkl
from collections import Counter
import operator
from wordcloud import WordCloud
import nltk
import sys
import pandas as pd
import numpy as np

# Takes the inputted ASIN and finds the top occuring adjectives
def word_freq(input):
    data = load_pkl("pickles/data.pkl")
    ASIN = input
    df = pd.DataFrame(data)
    # Get the asins and reviews in a list together
    var = df[(df['asin'] == ASIN) & ('reviewText' in df.keys())]
    var = var[['asin', 'reviewText']]
    train_data = np.array(var)
    asin_review = train_data.tolist()
    counter = Counter()
    # Get a count of every word in every review associated with that book
    for i in asin_review:
        split_word = nltk.word_tokenize(str(i[1]))
        tokens = nltk.pos_tag(split_word)
        adj = [x.lower() for x, key in tokens if (key == 'JJ')]
        counter = counter + Counter(adj)
    # Take the words with the top 100 occurences
    top_items = dict(sorted(counter.items(), key = operator.itemgetter(1), reverse = True)[:100])
    return top_items

# Takes the list of words and frequencies and creates a wordcloud out of it 
def word_cloud(asin):
    top_items = word_freq(asin)
    # Output time is limited by the height and width (resolution of image)
    wordcloud = WordCloud(background_color="white", height=450, width=564).generate_from_frequencies(top_items)
    wordcloud.to_file('word_cloud.png')

#word_cloud('000105001X')
#word_cloud('0001844423')
