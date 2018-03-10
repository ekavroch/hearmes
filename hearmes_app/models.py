from django.db import models
import requests
from collections import namedtuple
import json
import urllib.parse

# from gensim.summarization import summarize
#
# text = "Thomas A. Anderson is a man living two lives. By day he is an average computer programmer and by night a hacker known as Neo. Neo has always questioned his reality, but the truth is far beyond his imagination. Neo finds himself targeted by the police when he is contacted by Morpheus, a legendary computer hacker branded a terrorist by the government. Morpheus awakens Neo to the real world, a ravaged wasteland where most of humanity have been captured by a race of machines that live off of the humans' body heat and electrochemical energy and who imprison their minds within an artificial reality known as the Matrix. As a rebel against the machines, Neo must return to the Matrix and confront the agents: super-powerful computer programs devoted to snuffing out Neo and the entire human rebellion. "
# print('Summary:')
# print(summarize(text))

# from newspaper import Article
#
# def news_article_parser():
#     url="http://money.cnn.com/2018/03/09/news/economy/trump-tariffs-global-reaction/index.html"
#     article = Article(url)
#     # Definte article URL and create Article object using Article function
#     article.download()  # Download the article
#     article.html  # Print HTML of article
#     article.parse()  # Parse the HTML file
#     article.text = "By day he is an average computer programmer and by night a hacker known as Neo. Neo has always questioned his reality, but the truth is far beyond his imagination.Neo finds himself targeted by the police when he is contacted by Morpheus, a legendary computer hacker branded a terrorist by the government.Morpheus awakens Neo to the real world, a ravaged wasteland where most of humanity have been captured by a race of machines that live off of the humans' body heat and electrochemical energy and who imprison their minds within an artificial reality known as the Matrix."
#     article.title = "Neo the computer programmer"
#     article.nlp()
#     print(article.keyword)
#     print(article.summary)
#
# news_article_parser()

# Create your models here.
#TODO: Model to upload document & details: Name, Birthdate, Document
class Migrant(models.Model):
    migrant_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    age = models.CharField(max_length=3)
    job = models.CharField(max_length=30)
    message_text = models.CharField(max_length=255, null=True)
    message_img_path = models.CharField(max_length=255, null=True)
    tags = models.CharField(max_length=255, null=True)
    date = models.CharField(max_length=30, null=True)
    anonymity = models.CharField(max_length=30, null=True)

def uploadFormToDB(form_details):

    dump = json.dumps(form_details)
    data = json.loads(dump, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    try:
        # p = Migrant(first_name="Daren", last_name="Tan", age="22", profession="Data Scientist", message_img_path="hehe", anonymity="false")
        p = Migrant(first_name=data.first_name, last_name=data.last_name, destination = data.destination, age=data.age, job=data.job,
                    message_img_path=data.story_url, tags=data.tags, data=data.date)
        p.save()
    except Exception as e:
        return e

    m = Migrant.objects.latest('migrant_id')

    return m

#TODO: Model to change JPG to Computer Text
def JPEGtoText():
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Cursive_Writing_on_Notebook_paper.jpg/800px-Cursive_Writing_on_Notebook_paper.jpg"
    ocr_subscription_key = "e3ce4c5f3d254832b89e0e0e996ecb8f"
    ocr_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v1.0/"

    text_recognition_url = ocr_base_url + "RecognizeText"
    print(text_recognition_url)

    headers = {'Ocp-Apim-Subscription-Key': ocr_subscription_key}
    params = {'handwriting': True}
    data = {'url': image_url}
    response = requests.post(text_recognition_url, headers=headers, params=params, json=data)
    response.raise_for_status()

    operation_url = response.headers["Operation-Location"]

    import time

    analysis = {}
    while not "recognitionResult" in analysis:
        response_final = requests.get(response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        time.sleep(1)

    full_text = ""
    for line in analysis["recognitionResult"]["lines"]:
        full_text += line['text']

    return full_text

#Model for transalation
def translate (target, text):
    payload = {'to': target, 'text': urllib.parse.quote(text)}
    headers = {'Ocp-Apim-Subscription-Key': 'b0e5aa9d010346e2954b4ff20087b6dd'}
    response = requests.get('https://api.microsofttranslator.com/V2/Http.svc/Translate', params=payload, headers=headers)
    return response.text

#Model for sentiment and keywords detection
def analyzeStory(story):
    #URLS
    text_analytics_base_url = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0/"
    language_api_url = text_analytics_base_url + "languages"
    key_phrase_api_url = text_analytics_base_url + "keyPhrases"
    sentiment_api_url = text_analytics_base_url + "sentiment"

    headers = {"Ocp-Apim-Subscription-Key": 'dac80f6bdc41438dbb9dcc1c9a81b3e1'}
    sentiment_response = requests.post(sentiment_api_url, headers=headers, json=story)
    key_phrases_response = requests.post(key_phrase_api_url, headers=headers, json=story)
    key_phrases = key_phrases_response.json()
    sentiment = key_phrases_response.json()
    return key_phrases, sentiment

#TODO: Model to get 2 sentences
def split_sentences(text, delimiter):
    return text.split(delimiter)

def get_top_sentence(text, keywords, n):
    counter = 1
    result = []
    sentences_list = split_sentences(text, '.')
    for sentence in reversed(sentences_list):
        for keyword in reversed(keywords):
            if (keyword in sentence) and (sentence not in result):
                result.append(sentence.strip())
                if counter == n:
                    return result[::-1]
                else:
                    counter = counter + 1
                    break

#TODO: Model to upload to database
def updateDB(id, field, value):

    m = Migrant.objects.filter(pk=id)
    setattr(m, field, value)  # f.foo=bar
    m.save()

def retrieveEntity(id):
    return Migrant.objects.filter(pk=id)

#TODO: Model to retrive from database based on tags

#TEST
def news_article_parser(url):
    article = Article(url)
    # Definte article URL and create Article object using Article function
    article.download()  # Download the article
    article.html  # Print HTML of article
    article.parse()  # Parse the HTML file
    print(article)
    article.nlp()

    return article


news_article_parser("https://www.thestar.com.my/news/nation/2018/03/09/ec-submits-final-report-on-redelineation-to-pm/")