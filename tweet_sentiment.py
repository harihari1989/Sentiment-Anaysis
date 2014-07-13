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

def computeTweetSentiments(tweet, sentiment_scores):
	"""
		Function: computeTweetSentiments
		Parameters:
			tweet : The tweet text to be scored based on the sentiment_scores.
			sentiment_scores: A dictionary of sentiment words and their associated scores.
		Description:
			Scans for the words (unigrams, bigrams, trigrams) in the tweet and computes the sentiment score for the tweet
			as the sum of the individual terms.
		Returns:
			The sentiment score for the tweet.
	"""
	tweet_words = tweet.split()
	sent_sum = 0
	trigram = []
	bigram = []
	i = 0
	while i < len(tweet_words):
		if i+2 < len(tweet_words):
			trigram = [tweet_words[i], tweet_words[i+1], tweet_words[i+2]]
			triword = " ".join(trigram)
			if triword in sentiment_scores:
				sent_sum += sentiment_scores[triword]
				i += 3
				continue
		if i+1 < len(tweet_words):
			bigram = [tweet_words[i], tweet_words[i+1]]
			biword = " ".join(bigram)
			if biword in sentiment_scores:
				sent_sum += sentiment_scores[biword]
				i += 2
				continue
		sent_sum += sentiment_scores.get(tweet_words[i], 0)
		i += 1
	return sent_sum

def main():
	"""
		Usage: python tweet_sentiment.py <AFINNWordFile> <TweetFile>
	"""
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	sent_scores = {}
	sent_scores = constructSentimentScores(sent_file)
	for line in tweet_file:
		tweets = json.loads(line)
		if 'text' in tweets:
			tweet_text = tweets['text']
			print computeTweetSentiments(tweet_text, sent_scores)
		else:
			print 0

if __name__ == '__main__':
	main()
