import sys
import json
import re


def constructSentimentScores(sentiment_file):
	"""
		Function: constructSentimentScores
		Parameters:
			sentiment_file: Reference to the sentiment score file
		Description:
			Parses the sentiment file and returns a dictonary of sentiment text
			and their scores.
		Returns:
			A dictionary with sentiment terms as key and their associated scores as the value.
	"""
	scores = {} # initialize an empty dictionary
	for line in sentiment_file:
		term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
		scores[term] = int(score)  # Convert the score to an integer.
	return scores

def computeTweetSentimentsAndConstructNonAFINNWords(tweet, sentiment_scores):
	"""
		Function: computeTweetSentiments
		Parameters:
			tweet : The tweet text to be scored based on the sentiment_scores.
			sentiment_scores: A dictionary of sentiment words and their associated scores.
		Description:
			Scans for the words (unigrams, bigrams, trigrams) in the tweet and computes the sentiment score for the tweet
			as the sum of the individual terms.
		Returns:
			The sentiment score for the tweet and a list of words in the tweet which do not appear in the AFINN words.
	"""
	tweet_words = tweet.split()
	sent_sum = 0
	un_afinn_words = []
	i = 0
	while i < len(tweet_words):
		tweet_sent_score = sentiment_scores.get(tweet_words[i])
		if tweet_sent_score:
			sent_sum += tweet_sent_score
		else:
			un_afinn_words.append(tweet_words[i])
		i += 1
	return sent_sum, un_afinn_words

def main():
	"""
		Usage: python term_sentiment.py <AFINNWordFile> <TweetFile>
	"""
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	sent_scores = {}
	un_afinn_word_sent_score = {}
	un_afinn_word_occurence = {}
	sent_scores = constructSentimentScores(sent_file)
	for line in tweet_file:
		tweets = json.loads(line)
		if 'text' in tweets:
			tweet_text = tweets['text']
			(sent_score, un_afinn_words) = computeTweetSentimentsAndConstructNonAFINNWords(tweet_text, sent_scores)
			for un_afinn_word in un_afinn_words:
				un_afinn_word_sent_score[un_afinn_word] = un_afinn_word_sent_score.get(un_afinn_word, 0) + sent_score
				un_afinn_word_occurence[un_afinn_word] = un_afinn_word_occurence.get(un_afinn_word, 0) + 1
	for word in un_afinn_word_sent_score:
		un_afinn_word_sent_score[word] = float(un_afinn_word_sent_score[word])/un_afinn_word_occurence[word]
	for word in un_afinn_word_sent_score:
		print word," ",un_afinn_word_sent_score[word]
if __name__ == '__main__':
	main()
