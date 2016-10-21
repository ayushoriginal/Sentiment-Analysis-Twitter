# Sentiment-Analysis-Twitter

##    -Ayush Pareek

[![Join the chat at https://gitter.im/Sentiment-Analysis-Twitter/Lobby](https://badges.gitter.im/Sentiment-Analysis-Twitter/Lobby.svg)](https://gitter.im/Sentiment-Analysis-Twitter/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


Microblogging today has become a very popular communication tool among Internet users. Millions of messages are appearing daily in popular web-sites that provide services for microblogging such as Twitter, Tumblr, Facebook. Authors of those messages write about their life, share opinions on variety of topics and discuss current issues. Because of a free format of messages and an easy accessibility
of microblogging platforms, Internet users tend to shift from traditional communication tools (such as traditional blogs or mailing lists) to microblogging services. As more and more users post about products and services they use, or express their political and religious views, microblogging web-sites become valuable sources of people’s opinions and sentiments. Such data can be efficiently used
for marketing or social studies.[1]

![Political Sentiments](http://i.imgur.com/KtsvI4f.jpg)
<!--![Sentiments](http://i.imgur.com/57Yhewq.png)-->


##  1  Introduction

###  1.1 Applications of  Sentiment Analysis
Sentiment Analysis finds its application in a variety of domains.

**Business**
     Businesses may use sentiment analysis on blogs, review websites etc. to judge the market response of a product. This information may also be used for intelligent placement of advertisements. For example, if product "A" and "B" are competitors and an online merchant business "M" sells both, then "M" may advertise for "A" if the user displays positive sentiments towards "A", its brand or related products, or "B" if they display negative sentiments towards "A". 
     
**Financial Markets**
     Public opinion regarding companies can be used to predict performance of their stocks in the financial markets. If people have a positive opinion about a product that a company A has launched, then the share prices of A are likely to go higher and vice versa. Public opinion can be used as an additional feature in existing models that try to predict market performances based on historical data. 

**Government**
     Governments and politicians can actively monitor public sentiments as a response to their current policies, speeches made during campaigns etc. This will help them make create better public awareness regarding policies and even drive campaigns intelligently. 
     
![Sentiment Analysis can be useful to understand how the mood of the public affects election results](http://i.imgur.com/QI1IiDX.png)

Figure: Sentiment Analysis can be useful to understand how the mood of the public affects election results


### 1.2 Characteristic features of Tweets 

From the perspective of Sentiment
Analysis, we discuss a few characteristics of Twitter:

**Length of a Tweet**
     The maximum length of a Twitter message is 140 characters. This means that we can practically consider a tweet to be a single sentence, void of complex grammatical constructs. This is a vast difference from traditional subjects of Sentiment Analysis, such as movie reviews. 
     
**Language used**
     Twitter is used via a variety of media including SMS and mobile phone apps. Because of this and the 140-character limit, language used in Tweets tend be more colloquial, and filled with slang and misspellings. Use of hashtags also gained popularity on Twitter and is a primary feature in any given tweet. Our analysis shows that there are approximately 1-2 hashtags per tweet, as shown in Table 3 . 
     
**Data availability**
     Another difference is the magnitude of data available. With the Twitter API, it is easy to collect millions of tweets for training. There also exist a few datasets that have automatically and manually labelled the tweets [2] [3]. 
     
**Domain of topics**
     People often post about their likes and dislikes on social media. These are not al concentrated around one topic. This makes twitter a unique place to model a generic classifier as opposed to domain specific classifiers that could be build datasets such as movie reviews. 
     
     
## 2  Related Work

### 2.1 [Go, Bhayani and Huang (2009)](http://www-cs.stanford.edu/people/alecmgo/papers/TwitterDistantSupervision09.pdf)

 They classify Tweets for a query term into negative or positive sentiment. They collect training dataset automatically from Twitter. To collect positive and negative tweets, they query twitter for happy and sad emoticons.
 
 * Happy emoticons are different versions of smiling face, like ":)", ":-)", ": )", ":D", "=)" etc.
 * Sad emoticons include frowns, like ":(", ":-(", ":(" etc.
 
They try various features – unigrams, bigrams and Part-of-Speech and train their classifier on various machine learning algorithms – Naive Bayes, Maximum Entropy and Scalable Vector Machines and compare it against a baseline classifier by counting the number of positive and negative words from a publicly available corpus. They report that Bigrams alone and Part-of-Speech Tagging are not helpful and that Naive Bayes Classifier gives the best results.

### 2.2 [Pak and Paroubek (2010)](https://pdfs.semanticscholar.org/ad8a/7f620a57478ff70045f97abc7aec9687ccbd.pdf)

They identify that use of informal and creative language make sentiment analysis of tweets a rather different task . They leverage previous work done in hashtags and sentiment analysis to build their classifier. They use Edinburgh Twitter corpus to find out most frequent hashtags. They manually classify these hashtags and use them to in turn classify the tweets. Apart from using n-grams and Part-of-Speech features, they also build a feature set from already existing MPQA subjectivity lexicon and Internet Lingo Dictionary. They report that the best results are seen with n-gram features with lexicon features, while using Part-of-Speech features causes a drop in accuracy.

### 2.3 [Koulompis, Wilson and Moore (2011)](http://www.aclweb.org/website/old_anthology/S/S13/S13-2.pdf#page=526)

They identify that use of informal and creative language make sentiment analysis of tweets a rather different task [5]. They leverage previous work done in hashtags and sentiment analysis to build their classifier. They use Edinburgh Twitter corpus to find out most frequent hashtags. They manually classify these hashtags and use them to in turn classify the tweets. Apart from using n-grams and Part-of-Speech features, they also build a feature set from already existing MPQA subjectivity lexicon and Internet Lingo Dictionary. They report that the best results are seen with n-gram features with lexicon features, while using Part-of-Speech features causes a drop in accuracy.

### 2.3 [Saif, He and Alani (2012)](http://oro.open.ac.uk/34929/1/76490497.pdf)

They discuss a semantic based approach to identify the entity being discussed in a tweet, like a person, organization etc. They also demonstrate that removal of stop words is not a necessary step and may have undesirable effect on the classifier.


All of the aforementioned techniques rely on n-gram features. It is unclear that the use of Part-of-Speech tagging is useful or not. To improve accuracy, some employ different methods of feature selection or leveraging knowledge about micro-blogging. In contrast, we improve our results by using more basic techniques used in Sentiment Analysis, like stemming, two-step classification and negation detection and scope of negation.

Negation detection is a technique that has often been studied in sentiment analysis. Negation words like “not”, “never”, “no” etc. can drastically change the meaning of a sentence and hence the sentiment expressed in them. Due to presence of such words, the meaning of nearby words becomes opposite. Such words are said to be in the scope of negation. Many researches have worked on detecting the scope of negation.

The scope of negation of a cue can be taken from that word to the next following punctuation. Councill, McDonald and Velikovich (2010) discuss a technique to identify negation cues and their scope in a sentence. They identify explicit negation cues in the text and for each word in the scope. Then they find its distance from the nearest negative cue on the left and right.

##  3  Approach

We use different feature sets and machine learning classifiers to determine
the best combination for sentiment analysis of twitter. We also experiment
with various pre-processing steps like - punctuations, emoticons, twitter
specific terms and stemming. We investigated the following features -
unigrams, bigrams, trigrams and negation detection. We finally train our
classifier using various machine-learning algorithms - Naive Bayes, Decision
Trees and Maximum Entropy.

![Ayush's Approach](http://i.imgur.com/mXBzrNU.png)

We use a modularized approach with feature extractor and classification
algorithm as two independent components. This enables us to experiment with
different options for each component.

###  3.1  Datasets

One of the major challenges in Sentiment Analysis of Twitter is to collect a
labelled dataset. Researchers have made public the following datasets for
training and testing classifiers.

####  3.1.1  Twitter Sentiment Corpus

This is a collection of 5513 tweets collected for four different topics,
namely, Apple, Google, Microsoft, Twitter It is collected and hand-classified
by Sanders Analytics LLC. Each entry in the corpus contains, Tweet id,
Topic and a Sentiment label. We use Twitter-Python library to enrich this data
by downloading data like Tweet text, Creation Date, Creator etc. for every
Tweet id. Each Tweet is hand classified by an American male into the following
four categories. For the purpose of our experiments, we consider Irrelevant
and Neutral to be the same class. Illustration of Tweets in this corpus is
show in Table 1 .

- **Positive**
     For showing positive sentiment towards the topic
     
- **Positive**
     For showing no or mixed or weak sentiments towards the topic
     
- **Negative**
     For showing negative sentiment towards the topic
     
- **Irrelevant**
     For non English text or off-topic comments
     

<div style="text-align:center">
<table border="1">
<tr><td align="left">Class </td><td align="right">Count </td><td width="0">Example </td></tr>
<tr><td align="left">neg </td><td align="right">529 </td><td width="0">#Skype often crashing: #microsoft, what are you doing? </td></tr>
<tr><td align="left">neu </td><td align="right">3770 </td><td width="0">How #Google Ventures Chooses Which Startups Get Its $200
                Million http://t.co/FCWXoUd8 via @mashbusiness @mashable </td></tr>
<tr><td align="left">pos </td><td align="right">483 </td><td width="0">Now all @Apple has to do is get swype on the iphone and
                it will be crack. Iphone that is </td></tr></table>


<div class="p"><!----></div>
<div style="text-align:center">Table 1: Twitter Sentiment Corpus</div>
<a id="tab:TSC">
</a>
</div>

####  3.1.2  Stanford Twitter

This corpus of tweets, developed by Sanford’s Natural Language processing
research group, is publically available. The training set is collected by
querying Twitter API for happy emoticons like "`:)`" and sad emoticons like
"`:(`" and labelling them positive or negative. The emoticons were then
stripped and Re-Tweets and duplicates removed. It also contains around 500
tweets manually collected and labelled for testing purposes. We randomly
sample and use 5000 tweets from this dataset. An example of Tweets in this
corpus are shown in Table 2 .

<div style="text-align:center">
<table border="1">
<tr><td align="left">Class </td><td align="right">Count </td><td width="0">Example </td></tr>
<tr><td align="left">neg </td><td align="right">2501 </td><td width="0">Playing after the others thanks to TV scheduling may well allow us to know what's go on, but it makes things look bad on Saturday nights  </td></tr>
<tr><td align="left">pos </td><td align="right">2499 </td><td width="0">@francescazurlo HAHA!!! how long have you been singing that song now? It has to be at least a day. i think you're wildly entertaining!  </td></tr></table>


<div class="p"><!----></div>
<div style="text-align:center">Table 2: Stanford Corpus</div>
<a id="tab:STAN">
</a>
</div>

###  3.2  Pre Processing

User-generated content on the web is seldom present in a form usable for
learning. It becomes important to normalize the text by applying a series of
pre-processing steps. We have applied an extensive set of pre-processing steps
to decrease the size of the feature set to make it suitable for learning
algorithms. Figure 2 illustrates various features seen in micro-blogging.
Table 3 illustrates the frequency of these features per tweet, cut by
datasets. We also give a brief description of pre-processing steps taken.

![Figure](http://i.imgur.com/KqJnVTx.png)

Figure: Illustration of a Tweet with various features

<div style="text-align:center">
<table border="1">
<tr><td align="left"></td><td colspan="2" align="center">Twitter Sentiment
 </td><td colspan="2" align="center">Stanford Corpus
 </td><td colspan="2" align="center">Both </td></tr>
<tr><td align="left">Features   </td><td colspan="1" align="center">Avg. </td><td colspan="1" align="center">Max.
            </td><td colspan="1" align="center">Avg. </td><td colspan="1" align="center">Max.
            </td><td colspan="1" align="center">Avg. </td><td colspan="1" align="center">Max. </td></tr>
<tr><td align="left">Handles        </td><td align="right">0.6761 </td><td align="right">8 </td><td align="right">0.4888 </td><td align="right">10 </td><td align="right">0.5804 </td><td align="right">10 </td></tr>
<tr><td align="left">Hashtags   </td><td align="right">2.0276 </td><td align="right">13 </td><td align="right">0.0282 </td><td align="right">11 </td><td align="right">1.0056 </td><td align="right">13 </td></tr>
<tr><td align="left">Urls       </td><td align="right">0.4431 </td><td align="right">4 </td><td align="right">0.0452 </td><td align="right">2 </td><td align="right">0.2397 </td><td align="right">4 </td></tr>
<tr><td align="left">Emoticons  </td><td align="right">0.0550 </td><td align="right">3 </td><td align="right">0.0154 </td><td align="right">4 </td><td align="right">0.0348 </td><td align="right">4 </td></tr>
<tr><td align="left">Words      </td><td align="right">14.4084 </td><td align="right">31 </td><td align="right">13.2056 </td><td align="right">33 </td><td align="right">13.7936 </td><td align="right">33 </td></tr></table>


<div class="p"><!----></div>
<div style="text-align:center">Table 3: Frequency of Features per Tweet</div>
<a id="tab:feat_freq">
</a>
</div>








## References
- [Pak, Alexander, and Patrick Paroubek. "Twitter as a Corpus for Sentiment Analysis and Opinion Mining." LREc. Vol. 10. 2010.][1]
- [Alec Go, Richa Bhayani, and Lei Huang. Twitter sentiment classification using distant supervision. _Processing_, pages 1-6, 2009.][2]
- [Niek Sanders. Twitter sentiment corpus. http://www.sananalytics.com/lab/twitter-sentiment/. Sanders Analytics.][3]


