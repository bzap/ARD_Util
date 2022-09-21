# ARD Util

This is a simple python utility to provide better insight on Amazon items and their reviews. It takes in sample Amazon review data (e.g. [the book data from here)](http://deepyeti.ucsd.edu/jianmo/amazon/index.html), compresses it, and processes it. 

The GUI is built with PyQt6 and provides: 
 - Translating an Amazon ASIN to the item name
 - Providing similar item recommendations based on similarities in review keywords
 - Generating a word-cloud image based on the frequency of adjectives in the reviews of an item
 
## Dependencies 
***PyQt6***
***pip***
- nltk 
	- requires running `nltk.download('punkt')` and `nltk.download('averaged_perceptron_tagger')` 
- lxml 
- bs4 
- wordcloud 
- mechanize 
- pandas
- numpy 

## Usage

Initial importing and compression of the data is done is done using `json_sampler.py `. Subsequently running the GUI  is then done using `gui.py `.

![enter image description here](https://raw.githubusercontent.com/bzap/amazon_review_data/master/ss.png?token=GHSAT0AAAAAABZBXH62PJFSQM5UXV25ZXCCYZLQFBQ)![enter image description here](https://raw.githubusercontent.com/bzap/amazon_review_data/master/ss2.png?token=GHSAT0AAAAAABZBXH62LUZZ3U5NFD7T5MTIYZLQFKQ)

