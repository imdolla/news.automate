# import NLTK libaries for building a text summarizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# import beautifulsoup4 and requests to retrieve text from URL
import requests
from bs4 import BeautifulSoup

# import Tesseract-OCR libaries for recognizing text in images
# Tesseract is an optical character recognition engine for various operating systems
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ASITUTCH\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Import Pillow libary that adds support for opening, manipulating, and saving different image file formats 
from PIL import Image

# a function to retrieve text from an URL
def get_url_text(url):
    # request to access the specified URL
    page = requests.get(url)
    # after accessing the URL, extract the page content and assign it as soup
    soup = BeautifulSoup(page.content, "lxml")
    # find the content (aka.soup) that is a text format -> join them -> assign it to text 
    # essentially just soup.text
    urltext = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return urltext

# a function to retrieve text from an Image
def get_img_text(img):
    # using Tesseract to recognize the image and convert it to string
    imgtext = pytesseract.image_to_string(img)
    return imgtext

# asks the user for either a URL or Image Filename
user = int(input('News URL or Image FileName? \n Press 0 for News URL. \n Press 1 for Image FileName. \n Input:'))
text = ''
img = ''

# if user presses 0, enter URL
if (user == 0):
    url = input('Enter the URL: \n')
    text = get_url_text(url)
# if user presses 1, enter image filename
elif (user == 1):
    # opening the image from its filename 
    img = input('Enter the image filename: ')
    Image.open(img)
    text = get_img_text(img)

# assign the stopwords (words such as is, an, a, the, for) that will be removed.
stopwords = set (stopwords.words('english')) 

# use a word tokenizer (aka. split large piece of text into words)
words = word_tokenize(text)

# use a sentence tokenizer (aka. split large piece of text into sentences)
sentences = sent_tokenize(text)

# keep a frequency record of words using a dictionary
freqTable = dict()

# keep a score of how much each word appears in the dictionary (note: take a look at stopwords)
for word in words:
    word = word.lower()
    if word in stopwords:
        continue
    if word in freqTable:
        freqTable [word] += 1
    else:
        freqTable [word] = 1 

# keep each sentence using a dictionary 
sentenceValue = dict()

# use a for loop to go through every sentences and check if the sentence contains 
# words that appear frequently as assigned by the frequncy table of words above
# depending on the words it contains and the frequency table, we will assign score to each sentence 
for sentence in sentences:
    for word, freq in freqTable.items():
        if word in sentence.lower():
            if sentence in sentenceValue:
                sentenceValue[sentence] += freq
            else: 
                sentenceValue[sentence] = freq

# assign value to each sentences
sumValues = 0
for sentence in sentenceValue:
    sumValues += sentenceValue[sentence]

# average the value of each sentence in regard to the original text
# essentially test how "important" each sentence is to the original text
average = int(sumValues/len(sentenceValue))

# print the summary
summary = ''
for sentence in sentences:
    if (sentence in sentenceValue) and (sentenceValue[sentence] > (average)):
        summary += "" + sentence
print(summary)

# import the classifier function from classifier
from classifier import predit_category

# import python 
import os

# assign predicted_category as the output from the function that predicts the category
predicted_category = predit_category(summary)

# a function to put a file into the folders
def file_to_folder(predit_category):
    save_path = r'C:\Users\ASITUTCH\Desktop\year 11\coding\python project\\' + predit_category
    file_name = input("Name the File: \n")
    completeName = os.path.join(save_path, file_name)
    file = open(completeName, 'w')
    file.write(summary)
    file.close()
    print(file_name + ' is now in: ' + predicted_category)

# ask the users if they want to label their news using the classifier or not
label = int(input('Label the News + Save to Later? \n Press 0 for Yes. \n Press 1 for No. \n Input:'))
# if user press 0, yes label + put into folder
if label == 0:
    predit_category(summary)
    print('Predicted Category: ' + predicted_category)
    file_to_folder(predit_category(summary))
# if user press 1, no label
elif label == 1:
    print("Python is at your service.")


# https://edition.cnn.com/2022/01/14/politics/us-intelligence-russia-false-flag/index.html





