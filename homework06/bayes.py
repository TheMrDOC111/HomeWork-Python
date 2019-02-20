from collections import Counter
import math


class NaiveBayesClassifier:
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y."""
        # {(aleks,spam): 1, (by,ham): 1, ..}
        lst = []
        for sentence, clss in zip(X, y):
            for word in sentence.split():
                lst.append((word, clss))
        self.words_labels = Counter(lst)

        # {ham: 6700, spam: 2000}
        self.counted_labels = dict(Counter(y))
        words = [word for sentence in X for word in sentence.split()]

        # {"hi": 4, "bye": 2, "am": 1....}
        self.counted_words = dict(Counter(words))

        self.model = {
            'labels': {},
            'words': {},
        }

        # {'ham': {'count_by_label': 47670, 'likelihood': 0.8669230769230769}, 'spam': {'count_by_label': 12358, 'likelihood': 0.13307692307692306}}
        for cur_label in self.counted_labels:
            params = {
                # Total count of words with label
                'count_by_label': self.count_words(cur_label),
                # Likelihood of labels *P(C)*
                'likelihood': self.counted_labels[cur_label] / len(y),
            }
            self.model['labels'][cur_label] = params

        for word in self.counted_words:
            params = {}

            for cur_label in self.counted_labels:
                # Smoothing likelihood *P(wi|C)*
                params[cur_label] = self.smoothing_likelihood(word, cur_label)

            self.model['words'][word] = params

    def predict(self, X):
        """ Perform labelification on an array of test vectors X. """
        answers_lst = []

        for sentence in X:
            words = sentence.split()
            likely_labels = []

            for cur_label in self.model['labels']:

                likelihood = self.model['labels'][cur_label]['likelihood']

                # Calculating lnP(C)
                total_score = math.log(likelihood, math.e)

                for word in words:
                    word_dict = self.model['words'].get(word, None)

                    if word_dict:
                        # Calcuting the sum of lnP(wi|C)
                        total_score += math.log(word_dict[cur_label], math.e)

                likely_labels.append((total_score, cur_label))

            # Maximum value between lnP(label|D)
            _, answer = max(likely_labels)
            answers_lst.append(answer)

        return answers_lst

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        count = len(y_test)
        correct = 0
        for i, answer in enumerate(self.predict(X_test)):
            if answer == y_test[i]:
                correct += 1

        return correct / count

    def smoothing_likelihood(self, word, cur_label):
        """ Returns the smoothed likelihood with the given word and label in loop. """
        nc = self.model['labels'][cur_label]['count_by_label']
        nic = self.words_labels.get((word, cur_label), 0)
        d = len(self.counted_words)
        alpha = self.alpha

        return (nic + alpha) / (nc + alpha * d)

    def count_words(self, cur_label):
        """ Returns the count of words with the given label. """
        count = 0

        for word, label_name in self.words_labels:
            if cur_label == label_name:
                count += self.words_labels[(word, cur_label)]

        return count
