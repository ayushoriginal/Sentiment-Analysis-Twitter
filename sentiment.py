"""
Sentiment Analysis of Twitter Feeds
@Ayush Pareek
"""

import sys, os, random
import nltk, re
import collections
import time

def get_time_stamp():
    return time.strftime("%y%m%d-%H%M%S-%Z")

def grid(alist, blist):
    for a in alist:
        for b in blist:
            yield(a, b)

TIME_STAMP = get_time_stamp()

NUM_SHOW_FEATURES = 100
SPLIT_RATIO = 0.9
FOLDS = 10
LIST_CLASSIFIERS = ['NaiveBayesClassifier', 'MaxentClassifier', 'DecisionTreeClassifier', 'SvmClassifier'] 
LIST_METHODS = ['1step', '2step']

def k_fold_cross_validation(X, K, randomise=False):
    if randomise: from random import shuffle; X=list(X); shuffle(X)
    for k in range(K):
        training = [x for i, x in enumerate(X) if i % K != k]
        validation = [x for i, x in enumerate(X) if i % K == k]
        yield training, validation

def getTrainingAndTestData(tweets, K, k, method, feature_set):
    add_ngram_feat = feature_set.get('ngram', 1)
    add_negtn_feat = feature_set.get('negtn', False)

    from functools import wraps
    import preprocessing

    procTweets = [(preprocessing.processAll(text, subject=subj, query=quer), sent) \
                  for (text, sent, subj, quer) in tweets]

    stemmer = nltk.stem.PorterStemmer()

    all_tweets = []
    for (text, sentiment) in procTweets:
        words = [word if (word[0:2] == '__') else word.lower() \
                 for word in text.split() \
                 if len(word) >= 3]
        words = [stemmer.stem(w) for w in words]
        all_tweets.append((words, sentiment))

    train_tweets = [x for i, x in enumerate(all_tweets) if i % K != k]
    test_tweets = [x for i, x in enumerate(all_tweets) if i % K == k]

    unigrams_fd = nltk.FreqDist()
    if add_ngram_feat > 1:
        n_grams_fd = nltk.FreqDist()

    for (words, sentiment) in train_tweets:
        unigrams_fd.update(words)
        if add_ngram_feat >= 2:
            words_bi = [','.join(map(str, bg)) for bg in nltk.bigrams(words)]
            n_grams_fd.update(words_bi)
        if add_ngram_feat >= 3:
            words_tri = [','.join(map(str, tg)) for tg in nltk.trigrams(words)]
            n_grams_fd.update(words_tri)

    sys.stderr.write('\nlen( unigrams ) = ' + str(len(unigrams_fd.keys())))

    unigrams_sorted = unigrams_fd.keys()
    if add_ngram_feat > 1:
        sys.stderr.write('\nlen( n_grams ) = ' + str(len(n_grams_fd)))
        ngrams_sorted = [k for (k, v) in n_grams_fd.items() if v > 1]
        sys.stderr.write('\nlen( ngrams_sorted ) = ' + str(len(ngrams_sorted)))

    def get_word_features(words):
        bag = {}
        words_uni = ['has(%s)' % ug for ug in words]
        if add_ngram_feat >= 2:
            words_bi = ['has(%s)' % ','.join(map(str, bg)) for bg in nltk.bigrams(words)]
        else:
            words_bi = []
        if add_ngram_feat >= 3:
            words_tri = ['has(%s)' % ','.join(map(str, tg)) for tg in nltk.trigrams(words)]
        else:
            words_tri = []

        for f in words_uni + words_bi + words_tri:
            bag[f] = 1
        return bag

    negtn_regex = re.compile(r"""(?:
        ^(?:never|no|nothing|nowhere|noone|none|not|
            havent|hasnt|hadnt|cant|couldnt|shouldnt|
            wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint
        )$
    )
    |
    n't
    """, re.X)

    def get_negation_features(words):
        INF = 0.0
        negtn = [bool(negtn_regex.search(w)) for w in words]
        left = [0.0] * len(words)
        prev = 0.0
        for i in range(len(words)):
            if negtn[i]:
                prev = 1.0
            left[i] = prev
            prev = max(0.0, prev - 0.1)
    
        right = [0.0] * len(words)
        prev = 0.0
        for i in reversed(range(len(words))):
            if negtn[i]:
                prev = 1.0
            right[i] = prev
            prev = max(0.0, prev - 0.1)
    
        return dict(zip(
            ['neg_l(' + w + ')' for w in words] + ['neg_r(' + w + ')' for w in words],
            left + right))

    def counter(func):
        @wraps(func)
        def tmp(*args, **kwargs):
            tmp.count += 1
            return func(*args, **kwargs)
        tmp.count = 0
        return tmp

    @counter
    def extract_features(words):
        features = {}
        word_features = get_word_features(words)
        features.update(word_features)
        if add_negtn_feat:
            negation_features = get_negation_features(words)
            features.update(negation_features)

        sys.stderr.write('\rfeatures extracted for ' + str(extract_features.count) + ' tweets')
        return features

    extract_features.count = 0

    if '1step' == method:
        v_train = nltk.classify.apply_features(extract_features, train_tweets)
        v_test = nltk.classify.apply_features(extract_features, test_tweets)
        return (v_train, v_test)

    elif '2step' == method:
        isObj = lambda sent: sent in ['neg', 'pos']
        makeObj = lambda sent: 'obj' if isObj(sent) else sent
        
        train_tweets_obj = [(words, makeObj(sent)) for (words, sent) in train_tweets]
        test_tweets_obj = [(words, makeObj(sent)) for (words, sent) in test_tweets]

        train_tweets_sen = [(words, sent) for (words, sent) in train_tweets if isObj(sent)]
        test_tweets_sen = [(words, sent) for (words, sent) in test_tweets if isObj(sent)]

        v_train_obj = nltk.classify.apply_features(extract_features, train_tweets_obj)
        v_train_sen = nltk.classify.apply_features(extract_features, train_tweets_sen)
        v_test_obj = nltk.classify.apply_features(extract_features, test_tweets_obj)
        v_test_sen = nltk.classify.apply_features(extract_features, test_tweets_sen)

        test_truth = [sent for (words, sent) in test_tweets]

        return (v_train_obj, v_train_sen, v_test_obj, v_test_sen, test_truth)

    else:
        return nltk.classify.apply_features(extract_features, all_tweets)

def trainAndClassify(tweets, classifier, method, feature_set, fileprefix):
    INFO = '_'.join([str(classifier), str(method)] + [str(k) + str(v) for (k, v) in feature_set.items()])
    if len(fileprefix) > 0 and '_' != fileprefix[0]:
        directory = os.path.dirname(fileprefix)
        if not os.path.exists(directory):
            os.makedirs(directory)
        realstdout = sys.stdout
        sys.stdout = open(fileprefix + '_' + INFO + '.txt', 'w')

    print(INFO)
    sys.stderr.write('\n' + '#' * 80 + '\n' + INFO)

    if 'NaiveBayesClassifier' == classifier:
        CLASSIFIER = nltk.classify.NaiveBayesClassifier
        def train_function(v_train):
            return CLASSIFIER.train(v_train)
    elif 'MaxentClassifier' == classifier:
        CLASSIFIER = nltk.classify.MaxentClassifier
        def train_function(v_train):
            return CLASSIFIER.train(v_train, algorithm='GIS', max_iter=10)
    elif 'SvmClassifier' == classifier:
        CLASSIFIER = nltk.classify.SvmClassifier
        def SvmClassifier_show_most_informative_features(self, n=10):
            print('unimplemented')
        CLASSIFIER.show_most_informative_features = SvmClassifier_show_most_informative_features
        def train_function(v_train):
            return CLASSIFIER.train(v_train)
    elif 'DecisionTreeClassifier' == classifier:
        CLASSIFIER = nltk.classify.DecisionTreeClassifier
        def DecisionTreeClassifier_show_most_informative_features(self, n=10):
            text = ''
            for i in range(1, 10):
                text += str(i) + ': ' + str(self.tree[i]) + '\n'
            print(text)
        CLASSIFIER.show_most_informative_features = DecisionTreeClassifier_show_most_informative_features
        def train_function(v_train):
            return CLASSIFIER.train(v_train)

    for (k, v) in feature_set.items():
        sys.stderr.write('\n' + str(k) + ' : ' + str(v))

    results = []
    for (k, v) in k_fold_cross_validation(tweets, K=FOLDS):
        v_train, v_test = getTrainingAndTestData(v, FOLDS, k, method, feature_set)
        classifier = train_function(v_train)
        if method == '1step':
            acc = nltk.classify.accuracy(classifier, v_test)
            results.append(acc)
            sys.stderr.write('\naccuracy = ' + str(acc))
        else:
            v_test_obj, v_test_sen, test_truth = v_test
            acc_obj = nltk.classify.accuracy(classifier, v_test_obj)
            acc_sen = nltk.classify.accuracy(classifier, v_test_sen)
            results.append((acc_obj, acc_sen))
            sys.stderr.write('\naccuracy (objectivity) = ' + str(acc_obj))
            sys.stderr.write('\naccuracy (sentiment) = ' + str(acc_sen))

    if method == '1step':
        sys.stderr.write('\nmean accuracy = ' + str(sum(results) / len(results)))
    else:
        acc_obj = sum([r[0] for r in results]) / len(results)
        acc_sen = sum([r[1] for r in results]) / len(results)
        sys.stderr.write('\nmean accuracy (objectivity) = ' + str(acc_obj))
        sys.stderr.write('\nmean accuracy (sentiment) = ' + str(acc_sen))

    if len(fileprefix) > 0 and '_' != fileprefix[0]:
        sys.stdout.close()
        sys.stdout = realstdout

    return results

def main():
    if len(sys.argv) < 4:
        print("Usage: python sentiment.py <method> <classifier> <feature-set> <path-to-csv>")
        return

    method = sys.argv[1]
    classifier = sys.argv[2]
    feature_set = eval(sys.argv[3])  # make sure this is a safe operation
    csv_file_path = sys.argv[4]

    import pandas as pd

    try:
        tweets = pd.read_csv(csv_file_path, encoding='utf-8').values.tolist()
    except FileNotFoundError:
        sys.stderr.write(f"Error: The file '{csv_file_path}' was not found. Please check the path and try again.\n")
        return
    except Exception as e:
        sys.stderr.write(f"An error occurred: {e}\n")
        return

    results = trainAndClassify(tweets, classifier, method, feature_set, '')

if __name__ == "__main__":
    main()
