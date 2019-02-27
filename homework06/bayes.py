from collections import Counter
import math


class NaiveBayesClassifier:
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y."""
        lst = []
        for sentence, clss in zip(X, y):
            for word in sentence.split():
                lst.append((word, clss))
        self.words_labels = Counter(lst)
        print("words_labels", self.words_labels)
        self.counted_labels = dict(Counter(y))
        print("counted_labels", self.counted_labels)
        words = [word for sentence in X for word in sentence.split()]
        self.counted_words = dict(Counter(words))
        print("counted_words", self.counted_words)

        self.model = {
            'labels': {},
            'words': {},
        }

        for var_label in self.counted_labels:
            params = {
                'count_by_label': self.count_words(var_label),
                'likelihood': self.counted_labels[var_label] / len(y),
            }

            self.model['labels'][var_label] = params

        print("model", self.model)
        for word in self.counted_words:
            params = {}

            for var_label in self.counted_labels:
                params[var_label] = self.smoothing_likelihood(word, var_label)

            self.model['words'][word] = params

        print("model 2", self.model)

    def predict(self, X):
        """ Perform labelification on an array of test vectors X. """
        for sentence in X:
            words = sentence.split()
            likely_labels = []

            for cur_label in self.model['labels']:

                likelihood = self.model['labels'][cur_label]['likelihood']

                total_score = math.log(likelihood, math.e)

                for word in words:
                    word_dict = self.model['words'].get(word, None)

                    if word_dict:
                        total_score += math.log(word_dict[cur_label], math.e)

                likely_labels.append((total_score, cur_label))

            _, answer = max(likely_labels)
        return answer

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
        print(nc, nic, d)
        alpha = self.alpha

        return (nic + alpha) / (nc + alpha * d)

    def count_words(self, cur_label):
        """ Returns the count of words with the given label. """
        count = 0

        for word, label_name in self.words_labels:
            if cur_label == label_name:
                count += self.words_labels[(word, cur_label)]

        return count
