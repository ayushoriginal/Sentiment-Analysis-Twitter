import csv

queryTerms = {\
                'apple'     : ['@apple',    ],  \
                'microsoft' : ['#microsoft', ], \
                'google'    : ['#google', ],    \
                'twitter'   : ['#twitter', ],    \
    }

def getTweetsRawData( fileName ):
    # read all tweets and labels
    fp = open( fileName, 'rb' )
    reader = csv.reader( fp, delimiter=',', quotechar='"', escapechar='\\' )
    tweets = []
    for row in reader:
        tweets.append( [row[4], row[1], row[0], queryTerms[(row[0]).lower()] ] )
    # treat neutral and irrelevant the same
    for t in tweets:
        if (t[1] == 'positive'):
            t[1] = 'pos'
        elif (t[1] == 'negative'):
            t[1] = 'neg'
        elif (t[1] == 'irrelevant')|(t[1] == 'neutral'):
            t[1] = 'neu'

    return tweets # 0: Text # 1: class # 2: subject # 3: query

SampleTweetsStats = '''
   Class    Count Example
     neg      529 #Skype often crashing: #microsoft, what are you doing?
     neu     3770 How #Google Ventures Chooses Which Startups Get Its $200 Million http://t.co/FCWXoUd8 via @mashbusiness @mashable
     pos      483 Now all @Apple has to do is get swype on the iphone and it will be crack. Iphone that is
'''
