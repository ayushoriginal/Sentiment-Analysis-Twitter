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
LIST_CLASSIFIERS = [ 'NaiveBayesClassifier', 'MaxentClassifier', 'DecisionTreeClassifier', 'SvmClassifier' ] 
LIST_METHODS = ['1step', '2step']

def k_fold_cross_validation(X, K, randomise = False):
    """
    Generates K (training, validation) pairs from the items in X.

    Each pair is a partition of X, where validation is an iterable
    of length len(X)/K. So each training iterable is of length (K-1)*len(X)/K.

    If randomise is true, a copy of X is shuffled before partitioning,
    otherwise its order is preserved in training and validation.
    """
    if randomise: from random import shuffle; X=list(X); shuffle(X)
    for k in xrange(K):
        training = [x for i, x in enumerate(X) if i % K != k]
        validation = [x for i, x in enumerate(X) if i % K == k]
        yield training, validation

#X = [i for i in xrange(97)]
#for training, validation in k_fold_cross_validation(X, K=7):
#    for x in X: assert (x in training) ^ (x in validation), x


def getTrainingAndTestData(tweets, K, k, method, feature_set):

    add_ngram_feat = feature_set.get('ngram', 1)
    add_negtn_feat = feature_set.get('negtn', False)


    from functools import wraps
    import preprocessing

    procTweets = [ (preprocessing.processAll(text, subject=subj, query=quer), sent)    \
                        for (text, sent, subj, quer) in tweets]

    

    stemmer = nltk.stem.PorterStemmer()

    all_tweets = []                                             #DATADICT: all_tweets =   [ (words, sentiment), ... ]
    for (text, sentiment) in procTweets:
        words = [word if(word[0:2]=='__') else word.lower() \
                    for word in text.split() \
                    if len(word) >= 3]
        words = [stemmer.stem(w) for w in words]                #DATADICT: words = [ 'word1', 'word2', ... ]
        all_tweets.append((words, sentiment))

    # train_tweets = all_tweets[:int(len(all_tweets)*ratio)]      #DATADICT: train_tweets = [ (words, sentiment), ... ]
    # test_tweets  = all_tweets[int(len(all_tweets)*ratio):]      #DATADICT: test_tweets  = [ (words, sentiment), ... ]
    train_tweets = [x for i,x in enumerate(all_tweets) if i % K !=k]
    test_tweets  = [x for i,x in enumerate(all_tweets) if i % K ==k]

    unigrams_fd = nltk.FreqDist()
    if add_ngram_feat > 1 :
        n_grams_fd = nltk.FreqDist()

    for( words, sentiment ) in train_tweets:
        words_uni = words
        unigrams_fd.update(words)

        if add_ngram_feat>=2 :
            words_bi  = [ ','.join(map(str,bg)) for bg in nltk.bigrams(words) ]
            n_grams_fd.update( words_bi )

        if add_ngram_feat>=3 :
            words_tri  = [ ','.join(map(str,tg)) for tg in nltk.trigrams(words) ]
            n_grams_fd.update( words_tri )

    sys.stderr.write( '\nlen( unigrams ) = '+str(len( unigrams_fd.keys() )) )

    #unigrams_sorted = nltk.FreqDist(unigrams).keys()
    unigrams_sorted = unigrams_fd.keys()
    #bigrams_sorted = nltk.FreqDist(bigrams).keys()
    #trigrams_sorted = nltk.FreqDist(trigrams).keys()
    if add_ngram_feat > 1 :
        sys.stderr.write( '\nlen( n_grams ) = '+str(len( n_grams_fd )) )
        ngrams_sorted = [ k for (k,v) in n_grams_fd.items() if v>1]
        sys.stderr.write( '\nlen( ngrams_sorted ) = '+str(len( ngrams_sorted )) )

    def get_word_features(words):
        bag = {}
        words_uni = [ 'has(%s)'% ug for ug in words ]

        if( add_ngram_feat>=2 ):
            words_bi  = [ 'has(%s)'% ','.join(map(str,bg)) for bg in nltk.bigrams(words) ]
        else:
            words_bi  = []

        if( add_ngram_feat>=3 ):
            words_tri = [ 'has(%s)'% ','.join(map(str,tg)) for tg in nltk.trigrams(words) ]
        else:
            words_tri = []

        for f in words_uni+words_bi+words_tri:
            bag[f] = 1

        #bag = collections.Counter(words_uni+words_bi+words_tri)
        return bag

    negtn_regex = re.compile( r"""(?:
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
        negtn = [ bool(negtn_regex.search(w)) for w in words ]
    
        left = [0.0] * len(words)
        prev = 0.0
        for i in range(0,len(words)):
            if( negtn[i] ):
                prev = 1.0
            left[i] = prev
            prev = max( 0.0, prev-0.1)
    
        right = [0.0] * len(words)
        prev = 0.0
        for i in reversed(range(0,len(words))):
            if( negtn[i] ):
                prev = 1.0
            right[i] = prev
            prev = max( 0.0, prev-0.1)
    
        return dict( zip(
                        ['neg_l('+w+')' for w in  words] + ['neg_r('+w+')' for w in  words],
                        left + right ) )
    
    def counter(func):  #http://stackoverflow.com/questions/13512391/to-count-no-times-a-function-is-called
        @wraps(func)
        def tmp(*args, **kwargs):
            tmp.count += 1
            return func(*args, **kwargs)
        tmp.count = 0
        return tmp

    @counter    #http://stackoverflow.com/questions/13512391/to-count-no-times-a-function-is-called
    def extract_features(words):
        features = {}

        word_features = get_word_features(words)
        features.update( word_features )

        if add_negtn_feat :
            negation_features = get_negation_features(words)
            features.update( negation_features )
 
        sys.stderr.write( '\rfeatures extracted for ' + str(extract_features.count) + ' tweets' )
        return features

    extract_features.count = 0;

    
    if( '1step' == method ):
        # Apply NLTK's Lazy Map
        v_train = nltk.classify.apply_features(extract_features,train_tweets)
        v_test  = nltk.classify.apply_features(extract_features,test_tweets)
        return (v_train, v_test)

    elif( '2step' == method ):
        isObj   = lambda sent: sent in ['neg','pos']
        makeObj = lambda sent: 'obj' if isObj(sent) else sent
        
        train_tweets_obj = [ (words, makeObj(sent)) for (words, sent) in train_tweets ]
        test_tweets_obj  = [ (words, makeObj(sent)) for (words, sent) in test_tweets ]

        train_tweets_sen = [ (words, sent) for (words, sent) in train_tweets if isObj(sent) ]
        test_tweets_sen  = [ (words, sent) for (words, sent) in test_tweets if isObj(sent) ]

        v_train_obj = nltk.classify.apply_features(extract_features,train_tweets_obj)
        v_train_sen = nltk.classify.apply_features(extract_features,train_tweets_sen)
        v_test_obj  = nltk.classify.apply_features(extract_features,test_tweets_obj)
        v_test_sen  = nltk.classify.apply_features(extract_features,test_tweets_sen)

        test_truth = [ sent for (words, sent) in test_tweets ]

        return (v_train_obj,v_train_sen,v_test_obj,v_test_sen,test_truth)

    else:
        return nltk.classify.apply_features(extract_features,all_tweets)

def trainAndClassify( tweets, classifier, method, feature_set, fileprefix ):

    INFO = '_'.join( [str(classifier), str(method)] + [ str(k)+str(v) for (k,v) in feature_set.items()] )
    if( len(fileprefix)>0 and '_'!=fileprefix[0] ):
        directory = os.path.dirname(fileprefix)
        if not os.path.exists(directory):
            os.makedirs(directory)
        realstdout = sys.stdout
        sys.stdout = open( fileprefix+'_'+INFO+'.txt' , 'w')

    print INFO
    sys.stderr.write( '\n'+ '#'*80 +'\n' + INFO )

    if('NaiveBayesClassifier' == classifier):
        CLASSIFIER = nltk.classify.NaiveBayesClassifier
        def train_function(v_train):
            return CLASSIFIER.train(v_train)
    elif('MaxentClassifier' == classifier):
        CLASSIFIER = nltk.classify.MaxentClassifier
        def train_function(v_train):
            return CLASSIFIER.train(v_train, algorithm='GIS', max_iter=10)
    elif('SvmClassifier' == classifier):
        CLASSIFIER = nltk.classify.SvmClassifier
        def SvmClassifier_show_most_informative_features( self, n=10 ):
            print 'unimplemented'
        CLASSIFIER.show_most_informative_features = SvmClassifier_show_most_informative_features
        def train_function(v_train):
            return CLASSIFIER.train(v_train)
    elif('DecisionTreeClassifier' == classifier):
        CLASSIFIER = nltk.classify.DecisionTreeClassifier
        def DecisionTreeClassifier_show_most_informative_features( self, n=10 ):
            text = ''
            for i in range( 1, 10 ):
                text = nltk.classify.DecisionTreeClassifier.pp(self,depth=i)
                if len( text.split('\n') ) > n:
                    break
            print text
        CLASSIFIER.show_most_informative_features = DecisionTreeClassifier_show_most_informative_features
        def train_function(v_train):
            return CLASSIFIER.train(v_train, entropy_cutoff=0.05, depth_cutoff=100, support_cutoff=10, binary=False)

    accuracies = []
    if '1step' == method:
     for k in range(FOLDS):
        (v_train, v_test) = getTrainingAndTestData(tweets, FOLDS, k, method, feature_set)

        sys.stderr.write( '\n[training start]' )
        classifier_tot = train_function(v_train)
        sys.stderr.write( ' [training complete]' )
        
        print '######################'
        print '1 Step Classifier :', classifier
        accuracy_tot = nltk.classify.accuracy(classifier_tot, v_test)
        print 'Accuracy :', accuracy_tot
        print '######################'
        print classifier_tot.show_most_informative_features(NUM_SHOW_FEATURES)
        print '######################'

        # build confusion matrix over test set
        test_truth   = [s for (t,s) in v_test]
        test_predict = [classifier_tot.classify(t) for (t,s) in v_test]

        print 'Accuracy :', accuracy_tot
        print 'Confusion Matrix'
        print nltk.ConfusionMatrix( test_truth, test_predict )

        accuracies.append( accuracy_tot )
     print "Accuracies:", accuracies
     print "Average Accuracy:", sum(accuracies)/FOLDS


    elif '2step' == method:
        # (v_train, v_test) = getTrainingAndTestData(tweets,SPLIT_RATIO, '1step', feature_set)

        # isObj   = lambda sent: sent in ['neg','pos']
        # makeObj = lambda sent: 'obj' if isObj(sent) else sent

        # def makeObj_tweets(v_tweets):
        #     for (words, sent) in v_tweets:
        #         print sent, makeObj(sent)
        #         yield (words, makeObj(sent))
        # def getSen_tweets(v_tweets):
        #     for (words, sent) in v_tweets:
        #         print sent, isObj(sent)
        #         if isObj(sent):
        #             yield (words, sent)

        
        # v_train_obj = makeObj_tweets( v_train )
        # v_test_obj = makeObj_tweets( v_test )

        # v_train_sen = getSen_tweets( v_train )
        # v_test_sen = getSen_tweets( v_test )

     accuracies = []
     for k in range(FOLDS):
        (v_train_obj, v_train_sen, v_test_obj, v_test_sen, test_truth) = getTrainingAndTestData(tweets, FOLDS, k, method, feature_set)
        
        sys.stderr.write( '\n[training start]' )
        classifier_obj = train_function(v_train_obj)
        sys.stderr.write( ' [training complete]' )

        sys.stderr.write( '\n[training start]' )
        classifier_sen = train_function(v_train_sen)
        sys.stderr.write( ' [training complete]' )

        print '######################'
        print 'Objectivity Classifier :', classifier
        accuracy_obj = nltk.classify.accuracy(classifier_obj, v_test_obj)
        print 'Accuracy :', accuracy_obj
        print '######################'
        print classifier_obj.show_most_informative_features(NUM_SHOW_FEATURES)
        print '######################'

        test_truth_obj   = [s for (t,s) in v_test_obj]
        test_predict_obj = [classifier_obj.classify(t) for (t,s) in v_test_obj]

        print 'Accuracy :', accuracy_obj
        print 'Confusion Matrix'
        print nltk.ConfusionMatrix( test_truth_obj, test_predict_obj )
        
        print '######################'
        print 'Sentiment Classifier :', classifier
        accuracy_sen = nltk.classify.accuracy(classifier_sen, v_test_sen)
        print 'Accuracy :', accuracy_sen
        print '######################'
        print classifier_sen.show_most_informative_features(NUM_SHOW_FEATURES)
        print '######################'

        test_truth_sen   = [s for (t,s) in v_test_sen]
        test_predict_sen = [classifier_sen.classify(t) for (t,s) in v_test_sen]

        print 'Accuracy :', accuracy_sen
        print 'Confusion Matrix'
        if( len(test_truth_sen) > 0 ):
            print nltk.ConfusionMatrix( test_truth_sen, test_predict_sen )

        v_test_sen2 = [(t,classifier_obj.classify(t)) for (t,s) in v_test_obj]
        test_predict = [classifier_sen.classify(t) if s=='obj' else s for (t,s) in v_test_sen2]

        correct = [ t==p for (t,p) in zip(test_truth, test_predict)]
        accuracy_tot = float(sum(correct))/len(correct) if correct else 0

        print '######################'
        print '2 - Step Classifier :', classifier
        print 'Accuracy :', accuracy_tot
        print 'Confusion Matrix'
        print nltk.ConfusionMatrix( test_truth, test_predict )
        print '######################'

        classifier_tot = (classifier_obj, classifier_sen)
        accuracies.append( accuracy_tot )
     print "Accuracies:", accuracies
     print "Average Accuracy:", sum(accuracies)/FOLDS

    sys.stderr.write('\nAccuracies :')    
    for k in range(FOLDS):
        sys.stderr.write(' %0.5f'%accuracies[k])
    sys.stderr.write('\nAverage Accuracy: %0.5f\n'% (sum(accuracies)/FOLDS))
    sys.stderr.flush()
    
    sys.stdout.flush()
    if( len(fileprefix)>0 and '_'!=fileprefix[0] ):
        sys.stdout.close()
        sys.stdout = realstdout

    return classifier_tot

def main(argv) :
    __usage__='''
    usage: python sentiment.py logs/fileprefix ClassifierName,s methodName,s ngramVal,s negtnVal,s
        ClassifierName,s:   %s
        methodName,s:       %s
        ngramVal,s:         %s
        negtnVal,s:         %s
    ''' % ( str( LIST_CLASSIFIERS ), str( LIST_METHODS ), str([1,3]), str([0,1]) )
    import sanderstwitter02
    import stanfordcorpus
    import stats

    fileprefix = ''

    if (len(argv) >= 1) :
        fileprefix = str(argv[0])
    else :
        fileprefix = 'logs/run'

    classifierNames = []
    if (len(argv) >= 2) :
        classifierNames = [name for name in argv[1].split(',') if name in LIST_CLASSIFIERS]
    else :
        classifierNames = ['NaiveBayesClassifier']

    methodNames = []
    if (len(argv) >= 3) :
        methodNames = [name for name in argv[2].split(',') if name in LIST_METHODS]
    else :
        methodNames = ['1step']

    ngramVals = []
    if (len(argv) >= 4) :
        ngramVals = [int(val) for val in argv[3].split(',') if val.isdigit()]
    else :
        ngramVals = [ 1 ]

    negtnVals = []
    if (len(argv) >= 5) :
        negtnVals = [bool(int(val)) for val in argv[4].split(',') if val.isdigit()]
    else :
        negtnVals = [ False ]

    if (len( fileprefix )==0 or len( classifierNames )==0 or len( methodNames )==0 or len( ngramVals )==0 or len( negtnVals )==0 ):
        print __usage__
        return
    
    tweets1 = sanderstwitter02.getTweetsRawData('sentiment.csv')
    tweets2 = stanfordcorpus.getNormalisedTweets('stanfordcorpus/'+stanfordcorpus.FULLDATA+'.5000.norm.csv')
    #random.shuffle(tweets1)
    #random.shuffle(tweets2)
    tweets = tweets1 + tweets2
    random.shuffle( tweets )
    #tweets = tweets[:100]
    sys.stderr.write( '\nlen( tweets ) = '+str(len( tweets )) )

    #sys.stderr.write( '\n' )
    #stats.preprocessingStats( tweets1, fileprefix='logs/stats_'+TIME_STAMP+'/TSC' )
    #sys.stderr.write( '\n' )
    #stats.preprocessingStats( tweets2, fileprefix='')#logs/stats_'+TIME_STAMP+'/STAN' )
    #sys.stderr.write( '\n' )
    #stats.stepStats( tweets , fileprefix='logs/stats_'+TIME_STAMP+'/Both' )

    #generateARFF(tweets, fileprefix)

    #print classifierNames, methodNames, ngramVals, negtnVals
    TIME_STAMP = get_time_stamp()
    for (((cname, mname), ngramVal), negtnVal) in grid( grid( grid( classifierNames, methodNames), ngramVals ), negtnVals ):
        try:
            trainAndClassify(
                tweets, classifier=cname, method=mname,
                feature_set={'ngram':ngramVal, 'negtn':negtnVal},
                fileprefix=fileprefix+'_'+TIME_STAMP )
        except Exception, e:
            print e
    sys.stdout.flush()

if __name__ == "__main__":
    main(sys.argv[1:])
