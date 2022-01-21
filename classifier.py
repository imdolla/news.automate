# NEWS CLASSIFIER #

import os
# import the dataset that will be use to create the classifier model
from sklearn.datasets import fetch_20newsgroups

# import TF-IDF vectorizer (Term frequency - inverse document frequency)
# term frequency = number of times a term appears in a particular document
# inverse document frequency = measure how common or rare a term is across the entire collection of text 
# TF-IDF value of a term in a document is the product of TF and IDF, higher = the term is more relevant to the text
from sklearn.feature_extraction.text import TfidfVectorizer

# import the Multinomial Naive Bayes Classifier Algorithm
# Mainly use in Natural Language Processing (NLP) + predicts the tag of a text, calculates the
# probability of each tag for a given sample + gives the tag with the highest probability  
from sklearn.naive_bayes import MultinomialNB

# import a pipeline, allows sticking multiple processes into a single estimator 
from sklearn.pipeline import make_pipeline

# set our training data basing from the dataset imported above
data = fetch_20newsgroups()
categories = ['talk.politics.misc', 'sci.electronics', 'rec.autos', 'sci.med']
train = fetch_20newsgroups(subset='train', categories=categories)
test = fetch_20newsgroups(subset='test',categories=categories)

# create a pipeline model (TF-IDF Vectorizer + Multinomial Naive Bayes Classifier)
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
# Run our training data into the model
model.fit(train.data,train.target)

# function to run the summary through the classifier model created
def predit_category(s, train=train,model=model):
    pred = model.predict([s])
    predicted = train.target_names[pred[0]]
    return predicted

    

def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Creating Directory. " + directory)


for category in categories:
    create_folder(category)



