#@uthor: Ayush Pareek
import sys, time, os
import random, re, csv, collections
import nltk, pylab, numpy

import preprocessing

def printClassStats( tweets ):
    tweets_counter = collections.Counter( [t[1] for t in tweets] )
    print '%8s %8s %s' % ('Class', 'Count', 'Example')
    for (sent, count) in tweets_counter.items():
        print '%8s %8d %s' % (sent, count, random.choice([t for (t,s,_,_) in tweets if s==sent ]) )

def printFeaturesStats( tweets ):
    arr_Handles   = numpy.array( [0]*len(tweets) )
    arr_Hashtags  = numpy.array( [0]*len(tweets) )
    arr_Urls      = numpy.array( [0]*len(tweets) )
    arr_Emoticons = numpy.array( [0]*len(tweets) )
    arr_Words     = numpy.array( [0]*len(tweets) )
    arr_Chars     = numpy.array( [0]*len(tweets) )
    

    i=0
    for (text, sent, subj, quer) in tweets:
        arr_Handles[i]   = preprocessing.countHandles(text)
        arr_Hashtags[i]  = preprocessing.countHashtags(text)
        arr_Urls[i]      = preprocessing.countUrls(text)
        arr_Emoticons[i] = preprocessing.countEmoticons(text)
        arr_Words[i]     = len(text.split())
        arr_Chars[i]     = len(text)
        i+=1

    print '%-10s %-010s %-4s '%('Features',  'Average',            'Maximum')
    print '%10s %10.6f %10d'%('Handles',   arr_Handles.mean(),   arr_Handles.max()   )
    print '%10s %10.6f %10d'%('Hashtags',  arr_Hashtags.mean(),  arr_Hashtags.max()  )
    print '%10s %10.6f %10d'%('Urls',      arr_Urls.mean(),      arr_Urls.max()      )
    print '%10s %10.6f %10d'%('Emoticons', arr_Emoticons.mean(), arr_Emoticons.max() )
    print '%10s %10.6f %10d'%('Words',     arr_Words.mean(),     arr_Words.max()     )
    print '%10s %10.6f %10d'%('Chars',     arr_Chars.mean(),     arr_Chars.max()     )

def printReductionStats( tweets, function, filtering=True):
    if( function ):
        procTweets = [ (function(text, subject=subj, query=quer), sent)    \
                        for (text, sent, subj, quer) in tweets]
    else:
        procTweets = [ (text, sent)    \
                        for (text, sent, subj, quer) in tweets]
    tweetsArr = []
    for (text, sentiment) in procTweets:
        words = [word if(word[0:2]=='__') else word.lower() \
                        for word in text.split() \
                        if ( (not filtering) | (len(word) >= 3) ) ]
        tweetsArr.append([words, sentiment])
    # tweetsArr
    bag = collections.Counter()
    for (words, sentiment) in tweetsArr:
        bag.update(words)
    # unigram

    print '%20s %-10s %12d'% (
                ('None' if function is None else function.__name__),
                ( 'gte3' if filtering else 'all' ),
                sum(bag.values())
            )
    return True

def printAllRecuctionStats(tweets):
    print '%-20s %-10s %-12s'% ( 'Preprocessing', 'Filter', 'Words' )
    printReductionStats( tweets, None,                   False   )
    #printReductionStats( tweets, None,                   True    )
    printReductionStats( tweets, preprocessing.processHashtags,        True    )
    printReductionStats( tweets, preprocessing.processHandles,         True    )
    printReductionStats( tweets, preprocessing.processUrls,            True    )
    printReductionStats( tweets, preprocessing.processEmoticons,       True    )
    printReductionStats( tweets, preprocessing.processPunctuations,    True    )
    printReductionStats( tweets, preprocessing.processRepeatings,      True    )
    #printReductionStats( tweets, preprocessing.processAll,             False   )
    printReductionStats( tweets, preprocessing.processAll,             True    )

def printFreqDistCSV( dist, filename='' ):
    n_samples = len(dist.keys())
    n_repeating_samples = sum([ 1 for (k,v) in dist.items
        () if v>1 ])
    n_outcomes = dist._N
    print '%-12s %-12s %-12s'%( 'Samples', 'RepSamples', 'Outcomes' )
    print '%12d %12d %12d'%( n_samples, n_repeating_samples, n_outcomes )
    
    if( len(filename)>0 and '_'!=filename[0] ):
        with open( filename, 'w' ) as fcsv:
            distwriter = csv.writer( fcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC )
            
            for (key,value) in dist.items():
                distwriter.writerow( [key, value] ) #print key, '\t,\t', dist[key]

def preprocessingStats( tweets, fileprefix='' ):

    if( len(fileprefix)>0 and '_'!=fileprefix[0] ):
        directory = os.path.dirname(fileprefix)
        if not os.path.exists(directory):
            os.makedirs(directory)
        print 'writing to', fileprefix+'_stats.txt'
        realstdout = sys.stdout
        sys.stdout = open( fileprefix+'_stats.txt' , 'w')

    ###########################################################################  

    print 'for', len(tweets), 'tweets:'

    print '###########################################################################'

    printFeaturesStats( tweets )

    print '###########################################################################'

    printAllRecuctionStats( tweets )

    print '###########################################################################'

    procTweets = [ (preprocessing.processAll(text, subject=subj, query=quer), sent)    \
                        for (text, sent, subj, quer) in tweets]
    tweetsArr = []
    for (text, sentiment) in procTweets:
        words = [word if(word[0:2]=='__') else word.lower() \
                        for word in text.split() \
                        if ( (len(word) >= 3) ) ]
        tweetsArr.append([words, sentiment])
    unigrams_fd = nltk.FreqDist()
    bigrams_fd = nltk.FreqDist()
    trigrams_fd = nltk.FreqDist()
    for (words, sentiment) in tweetsArr:
        words_bi = [ ','.join(map(str,bg)) for bg in nltk.bigrams(words) ]
        words_tri  = [ ','.join(map(str,tg)) for tg in nltk.trigrams(words) ]
        unigrams_fd.update( words )
        bigrams_fd.update( words_bi )
        trigrams_fd.update( words_tri )

    print 'Unigrams Distribution'
    printFreqDistCSV(unigrams_fd, filename=fileprefix+'_1grams.csv')
    if( len(fileprefix)>0 and '_'!=fileprefix[0] ):
        pylab.show = lambda : pylab.savefig(fileprefix+'_1grams.pdf')
    unigrams_fd.plot(50, cumulative=True)
    pylab.close()

    print 'Bigrams Distribution'
    printFreqDistCSV(bigrams_fd, filename=fileprefix+'_2grams.csv')
    if( len(fileprefix)>0 and '_'!=fileprefix[0] ):
        pylab.show = lambda : pylab.savefig(fileprefix+'_2grams.pdf')
    bigrams_fd.plot(50, cumulative=True)
    pylab.close()

    print 'Trigrams Distribution'
    printFreqDistCSV(trigrams_fd, filename=fileprefix+'_3grams.csv')
    if( len(fileprefix)>0 and '_'!=fileprefix[0] ):
        pylab.show = lambda : pylab.savefig(fileprefix+'_3grams.pdf')
    trigrams_fd.plot(50, cumulative=True)
    pylab.close()

    if( len(fileprefix)>0 and '_'!=fileprefix[0] ):
        pylab.show = lambda : pylab.savefig(fileprefix+'_ngrams.pdf')
    unigrams_fd.plot(50, cumulative=True)
    bigrams_fd.plot(50, cumulative=True)
    trigrams_fd.plot(50, cumulative=True)
    pylab.close()    

    if( len(fileprefix)>0 and '_'!=fileprefix[0] ):
        sys.stdout.close()
        sys.stdout = realstdout

def stepStats( tweets, num_bins=10, split='easy', fileprefix='' ):
    tot_size = len(tweets)
    num_digits = len(str(tot_size))

    if split=='equal':
        sizes = [ int((r+1.0)/num_bins*tot_size) for r in range( num_bins ) ]
    elif split=='log':
        sizes = [ int(2**(math.log(tot_size,2)*(r+1.0)/num_bins) ) for r in range( num_bins ) ]
    else: # split=='easy'
        sizes = range( 0, tot_size, tot_size/num_bins)[1:]+[tot_size]

    for s in sizes:
        print 'processing stats for %d tweets'%s
        preprocessingStats( tweets[0:s], fileprefix+'_%0{0}d'.format(num_digits) % s )

def oldStats2CSV( in_file, fileprefix=''):
    if fileprefix == '':
        fileprefix = in_file.rstrip('_stats.txt')
    fp = open( in_file, 'r' )
    fq = open( fileprefix+'_statsnew.txt', 'w' )

    line = ''
    line_start = 0
    line_count = 20
    line_end   = line_start+line_count
    for line_num in range(line_start, line_end):   # write Statistics
        line = fp.readline()
        fq.write( line )

    for section in [1,2,3]:
        line_start = line_end
        line_count = 2
        line_end   = line_start+line_count
        for line_num in range( line_start, line_end ):
            line = fp.readline()
            fq.write( line )
    
        line_start = line_end
        line_count = [int(l) for l in line.split() if l.isdigit()][0]
        line_end = line_start+line_count
        fr = open( fileprefix+'_%dgrams.csv'%section, 'w')
        fwrt = csv.writer( fr, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC )
        for line_num in range( line_start, line_end ):  # write unigrams
            line = fp.readline()
            row = line.split('\t,\t')
            row[0] = row[0].strip()
            row[1] = int(row[1])
            fwrt.writerow( row )
        fr.close()

    fp.close()
    fq.close()

stats_tiltes = [
'"# tweets"',
'"avg(Handles)"',
'"max(Handles)"',
'"avg(Hashtags)"',
'"max(Hashtags)"',
'"avg(Urls)"',
'"max(Urls)"',
'"avg(Emoticons)"',
'"max(Emoticons)"',
'"avg(Words)"',
'"max(Words)"',
'"avg(Chars)"',
'"max(Chars)"',
'"preprocessing(None)"',
'"preprocessing(Hashtags)"',
'"preprocessing(Handles)"',
'"preprocessing(Urls)"',
'"preprocessing(Emoticons)"',
'"preprocessing(Punctuations)"',
'"preprocessing(Repeatings)"',
'"preprocessing(All)"',
'"Unigrams samples"',
'"Unigrams repeating samples"',
'"Unigrams outcomes"',
'"Bigrams samples"',
'"Bigrams repeating samples"',
'"Bigrams outcomes"',
'"Trigrams samples"',
'"Trigrams repeating samples"',
'"Trigrams outcomes"',
]

def newStats2CSV(files, out_file):

    arr = [ [] ] * len(files)

    for j in range( len(files)):
        values = []
        with open(files[j], 'r') as fp:
            for line in fp:
                values += [ float(w) for w in line.split()\
                                if  w[0] in ['0','1','2','3','4','5','6','7','8','9'] ]
        arr[j] = values

    with open(out_file, 'w') as fq:
        stats_writer = csv.writer( fq, delimiter=',', quotechar='\'')#, quoting=csv.QUOTE_NONE )
        for i in range(0,len(stats_tiltes)):
            row = [stats_tiltes[i]] + [arr[j][i] for j in range(len(files))]
            stats_writer.writerow( row )


filelist = [
'logs/stats_140617-214922-IST/Both_0978_stats.txt',
'logs/stats_140617-214922-IST/Both_1956_stats.txt',
'logs/stats_140617-214922-IST/Both_2934_stats.txt',
'logs/stats_140617-214922-IST/Both_3912_stats.txt',
'logs/stats_140617-214922-IST/Both_4890_stats.txt',
'logs/stats_140617-214922-IST/Both_5868_stats.txt',
'logs/stats_140617-214922-IST/Both_6846_stats.txt',
'logs/stats_140617-214922-IST/Both_7824_stats.txt',
'logs/stats_140617-214922-IST/Both_8802_stats.txt',
'logs/stats_140617-214922-IST/Both_9780_stats.txt',
'logs/stats_140617-214922-IST/Both_9782_stats.txt',
]


['0','1','2','3','4','5','6','7','8','9']
