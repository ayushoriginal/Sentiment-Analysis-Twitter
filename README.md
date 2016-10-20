# Sentiment-Analysis-Twitter

-Ayush Pareek

[![Join the chat at https://gitter.im/Sentiment-Analysis-Twitter/Lobby](https://badges.gitter.im/Sentiment-Analysis-Twitter/Lobby.svg)](https://gitter.im/Sentiment-Analysis-Twitter/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


Microblogging today has become a very popular communication tool among Internet users. Millions of messages are appearing daily in popular web-sites that provide services for microblogging such as Twitter, Tumblr, Facebook. Authors of those messages write about their life, share opinions on variety of topics and discuss current issues. Because of a free format of messages and an easy accessibility
of microblogging platforms, Internet users tend to shift from traditional communication tools (such as traditional blogs or mailing lists) to microblogging services. As more and more users post about products and services they use, or express their political and religious views, microblogging web-sites become valuable sources of people’s opinions and sentiments. Such data can be efficiently used
for marketing or social studies.[1]
[Political Sentiments](http://i.imgur.com/KtsvI4f.jpg)
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

### 2.1
Go, Bhayani and Huang (2009) were among the first to explore sentiment analysis on Twitter [2]. They classify Tweets for a query term into negative or positive sentiment. They collect training dataset automatically from Twitter. To collect positive and negative tweets, they query twitter for happy and sad emoticons. Happy emoticons are different versions of smiling face, like ":)", ":-)", ": )", ":D", "=)" etc. Sad emoticons include frowns, like ":(", ":-(", ":(" etc. They try various features – unigrams, bigrams and Part-of-Speech and train their classifier on various machine learning algorithms – Naive Bayes, Maximum Entropy and Scalable Vector Machines and compare it against a baseline classifier by counting the number of positive and negative words from a publicly available corpus. They report that Bigrams alone and Part-of-Speech Tagging are not helpful and that Naive Bayes Classifier gives the best results.

- Extract the fc-7 image features using:
```
python extract_fc7.py --split=train
python extract_fc7.py --split=val
```

- <b>Training</b>
  * Basic usage `python train.py`
  * Options
    - `rnn_size`: Size of LSTM internal state. Default is 512.
    - `num_lstm_layers`: Number of layers in LSTM
    - `embedding_size`: Size of word embeddings. Default is 512.
    - `learning_rate`: Learning rate. Default is 0.001.
    - `batch_size`: Batch size. Default is 200.
    - `epochs`: Number of full passes through the training data. Default is 50.
    - `img_dropout`:  Dropout for image embedding nn. Probability of dropping input. Default is 0.5.
    - `word_emb_dropout`: Dropout for word embeddings. Default is 0.5.
    - `data_dir`: Directory containing the data h5 files. Default is `Data/`.

- <b>Prediction</b>
  * ```python predict.py --image_path="sample_image.jpg" --question="What is the color of the animal shown?" --model_path = "Data/Models/model2.ckpt"```
  * Models are saved during training after each of the complete training data in ```Data/Models```. Supply the path of the trained model in ```model_path``` option.
  
- <b>Evaluation</b>
  * run `python evaluate.py` with the same options as that in train.py, if not the defaults.

## Implementation Details
- fc7 relu layer features from the pretrained VGG-16 model are used for image embeddings. I did not scale these features, and am not sure if that can make a difference.
- Questions are zero padded for fixed length questions, so that batch training may be used. Questions are represented as word indices of a question word vocabulary built during pre processing.
- Answers are mapped to 1000 word vocabulary, covering 87% answers across training and validation datasets.
- The LSTM+VIS model is defined in vis_lstm.py. The input tensors for training are fc7 features, Questions(Word indices upto 22 words), Answers(one hot encoding vector of size 1000). The model depicted in the figure is implemented with 2 LSTM layers by default(num_layers in configurable).

## Results
The model achieved an accuray of 50.8% on the validation dataset after 12 epochs of training across the entire training dataset.

## Sample Predictions

The fun part! Try it for yourself. Make sure you have tensorflow installed. Download the data files/trained model from [this link][9] and save them in the ```Data/``` directory. Also download the [pretrained VGG-16 model][7] and save it as ```Data/vgg16.tfmodel```. You can test for any sample image using:
```
python predict.py --image_path="Data/sample.jpg" --question="Which animal is this?" --model_path="Data/model2.ckpt"
```
| Image        | Question           | Top Answers (left to right)  |
| ------------- |:-------------:| -----:|
| ![](http://i.imgur.com/j4FiEaS.jpg)      | What color is the signal? | red, green, yellow|
| ![](http://i.imgur.com/FUR7k0y.jpg)      | What animal is this? | giraffe, cow, horse|
| ![](http://i.imgur.com/VrGUves.jpg)      | What animal is this? | cat, dog, giraffe|
| ![](http://i.imgur.com/yk53y1Y.jpg)      | What color is the frisbee that is in the dog's mouth? | white, brown, red|
| ![](http://i.imgur.com/yk53y1Y.jpg)      | What color is the frisbee that is upside down? | red, white, blue|
| ![](http://i.imgur.com/ifcccpd.jpg)      | What are they playing with? | frisbee, soccer ball, soccer|
| ![](http://i.imgur.com/VrjUbgH.jpg)      | What is in the standing person's hand? | bat, glove, ball|
| ![](http://i.imgur.com/80foxDZ.jpg)      | What are they doing? | surfing, swimming, parasailing|
| ![](http://i.imgur.com/7ZZi2Xp.jpg)      | What sport is this? | skateboarding, parasailing, surfing|

## References
- [Pak, Alexander, and Patrick Paroubek. "Twitter as a Corpus for Sentiment Analysis and Opinion Mining." LREc. Vol. 10. 2010.][1]
- [Alec Go, Richa Bhayani, and Lei Huang. Twitter sentiment classification using distant supervision. _Processing_, pages 1-6, 2009.][2]
- [Niek Sanders. Twitter sentiment corpus. http://www.sananalytics.com/lab/twitter-sentiment/. Sanders Analytics.][3]


