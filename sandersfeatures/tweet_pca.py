"""
@package tweet_pca
PCT for dimensionality reduction.

"""
import mdp, numpy
import tweet_features

import pdb


def tweet_pca_reduce( tweets_train, tweets_test, output_dim ):

    # convert dictionary feature vecs to numpy array
    print '--> Converting dictionaries to NumPy arrays'
    train_arr = numpy.array( [tweet_features.tweet_dict_to_nparr(t) for \
                              (t,s) in tweets_train])

    test_arr = numpy.array( [tweet_features.tweet_dict_to_nparr(t) for \
                             (t,s) in tweets_test])


    # compute principle components over training set
    print '--> Computing PCT'
    pca_array = mdp.pca( train_arr.transpose(), \
                         svd=True, output_dim=output_dim )


    # both train and test sets to PC space
    print '--> Projecting feature vectors to PC space'

    train_arr = numpy.dot( train_arr, pca_array )
    test_arr  = numpy.dot( test_arr,  pca_array )


    # convert projected vecs back to reduced dictionaries
    print '--> Converting NumPy arrays to dictionaries'

    reduced_train = \
        zip( [tweet_features.tweet_nparr_to_dict(v) for v in train_arr], \
             [s for (t,s) in tweets_train] )

    reduced_test  = \
        zip( [tweet_features.tweet_nparr_to_dict(v) for v in test_arr], \
             [s for (t,s) in tweets_test])

    return (reduced_train, reduced_test)
