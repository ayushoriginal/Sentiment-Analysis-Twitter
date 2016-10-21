"""
http://help.sentiment140.com/for-students

Format
Data file format has 6 fields:
0 - the polarity of the tweet (0 = negative, 2 = neutral, 4 = positive)
1 - the id of the tweet (2087)
2 - the date of the tweet (Sat May 16 23:58:44 UTC 2009)
3 - the query (lyx). If there is no query, then this value is NO_QUERY.
4 - the user that tweeted (robotickilldozr)
5 - the text of the tweet (Lyx is cool)

"""

FULLDATA = 'training.1600000.processed.noemoticon.csv'
TESTDATA = 'testdata.manual.2009.06.14.csv'

POLARITY= 0 # in [0,5]
TWID    = 1
DATE    = 2
SUBJ    = 3 # NO_QUERY
USER    = 4
TEXT    = 5

import csv, re, random

regex = re.compile( r'\w+|\".*?\"' )

def get_class( polarity ):
    if polarity in ['0', '1']:
        return 'neg'
    elif polarity in ['3', '4']:
        return 'pos'
    elif polarity == '2':
        return 'neu'
    else:
        return 'err'

def get_query( subject ):
    if subject == 'NO_QUERY':
        return []
    else:
        return regex.findall(subject)

def getAllQueries(in_file):

    fp = open(in_file , 'r')
    rd = csv.reader(fp, delimiter=',', quotechar='"' )

    queries = set([])

    for row in rd:
        queries.add(row[3])

    print queries

    for q in queries:
        print q, "\t",

    return queries

def sampleCSV( in_file, out_file, K=100 ):

    fp = open(in_file , 'r')
    fp2 = open(out_file , 'w')

    for i in range(0,K):
        line = fp.readline()
        fp2.write(line)

    fp.close()
    fp2.close()

    return 0

def randomSampleCSV( in_file, out_file, K=100 ):

    fp = open(in_file , 'r')
    fq = open(out_file, 'w')

    rows = [None] * K

    i = 0
    for row in fp:
        i+=1
        j = random.randint(1,i)
        if i < K:
            rows[i] = row
        elif j <= K:
            rows[j-1] = row

    for row in rows:
        fq.write(row)

    min(1, K/i)

def getNormalisedCSV( in_file, out_file ):
    fp = open(in_file , 'r')
    rd = csv.reader(fp, delimiter=',', quotechar='"' )

    fq = open(out_file, 'w')
    wr = csv.writer(fq, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL )

    for row in rd:
        queries = get_query(row[SUBJ])
        wr.writerow( [row[TEXT], get_class(row[POLARITY]), row[SUBJ]] + [len(queries)] + queries )

def getNormalisedTweets(in_file):
    fp = open(in_file , 'r')
    rd = csv.reader(fp, delimiter=',', quotechar='"' )
    #print in_file, countlines( in_file )

    tweets = []
    count = 0
    for row in rd:
        numQueries = int(row[3])
        tweets.append( row[:3] + [row[4:4+numQueries]] )
        count+=1

    #print count
    #print 'len(tweets) =', len(tweets)
    return tweets

def countlines( filename ):
    count = 0
    with open( filename, 'r' ) as fp:
        for line in fp:
            count+=1
    return count

#getAllQueries( 'testdata.manual.2009.06.14.csv' )
#getAllQueries( 'training.1600000.processed.noemoticon.csv' )

#randomSampleCSV(FULLDATA, FULLDATA+'.sample.csv')
#sampleCSV(TESTDATA, TESTDATA+'.sample.csv')

#getNormalisedCSV(FULLDATA+'.sample.csv', FULLDATA+'.norm.csv')

#randomSampleCSV(FULLDATA, FULLDATA+'.100000.sample.csv', K=100000)
#getNormalisedCSV(FULLDATA+'.100000.sample.csv', FULLDATA+'.100000.norm.csv')


SampleTweetsStats = '''
   Class    Count Example
     neg     2449 @jbrotherlove I thought it was a great love story 
     pos     2551 I hope that these kitchen renos don't last any longer... they are so annoying 
'''
