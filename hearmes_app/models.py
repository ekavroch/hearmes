from django.db import models
import requests
from collections import namedtuple
import json
import urllib.parse
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
import os

block_blob_service = BlockBlobService(account_name='hearmes', account_key='NZ/H80jO9ma8KsVS9pi0EFgZEj5FhYZYHaGqYg5/HKXP+EhWytB0JbUpWqktKqkfWnw89AwPp4//Q8YhZN6tqg==')

# Create your models here.
#TODO: Model to upload document & details: Name, Birthdate, Document
class Migrant(models.Model):
    migrant_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    age = models.CharField(max_length=3)
    job = models.CharField(max_length=30)
    message_text = models.CharField(max_length=600, null=True)
    message_img_path = models.CharField(max_length=255, null=True)
    tags = models.CharField(max_length=255, null=True)
    date = models.CharField(max_length=30, null=True)
    anonymity = models.CharField(max_length=30, null=True)
    sentiment = models.CharField(max_length=255, null=True)
    excerpt = models.CharField(max_length=255, null=True)

    def as_dict(self):
        return {
            "id": self.migrant_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "destination": self.destination,
            "age": self.age,
            "job": self.job,
            "message_text": self.message_text,
            "message_img_path": self.message_img_path,
            "tags": self.tags,
            "date": self.date,
            "anonymity": self.anonymity,
            "sentiment": self.sentiment,
            "excerpt": self.excerpt,
            "initials": self.first_name[0] + "." + self.last_name[0] + "."
        }

def uploadFormToDB(form_details):

    dump = json.dumps(form_details)
    data = json.loads(dump, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    try:
        # p = Migrant(first_name="Daren", last_name="Tan", age="22", profession="Data Scientist", message_img_path="hehe", anonymity="false")
        p = Migrant(first_name=data.first_name, last_name=data.last_name, destination = data.destination, age=data.age, job=data.job,
                    message_img_path=data.story_url, tags=data.tags, date=data.date)
        p.save()
    except Exception as e:
        return e

    m = Migrant.objects.latest('migrant_id')

    return m

#TODO: Model to change JPG to Computer Text
def JPEGtoText(image_url):
    img_name = image_url.rsplit('/', 1)[-1]
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(BASE_DIR)
    block_blob_service.create_blob_from_path(
        'stories',
        img_name,
        BASE_DIR + image_url,
    )

    ocr_subscription_key = "e3ce4c5f3d254832b89e0e0e996ecb8f"
    ocr_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v1.0/"

    text_recognition_url = ocr_base_url + "RecognizeText"
    print(text_recognition_url)

    headers = {'Ocp-Apim-Subscription-Key': ocr_subscription_key}
    params = {'handwriting': True}
    data = {'url': "https://hearmes.blob.core.windows.net/stories/"+img_name}
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
        full_text += line['text'] + ' '

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
    documents = {'documents': [
        {'id': '1', 'text': story},
    ]}

    text_analytics_base_url = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0/"
    language_api_url = text_analytics_base_url + "languages"
    key_phrase_api_url = text_analytics_base_url + "keyPhrases"
    sentiment_api_url = text_analytics_base_url + "sentiment"

    headers = {"Ocp-Apim-Subscription-Key": 'dac80f6bdc41438dbb9dcc1c9a81b3e1'}
    sentiment_response = requests.post(sentiment_api_url, headers=headers, json=documents)
    key_phrases_response = requests.post(key_phrase_api_url, headers=headers, json=documents)
    key_phrases = key_phrases_response.json()
    sentiment = sentiment_response.json()
    key_phrases = key_phrases['documents'][0]['keyPhrases']
    sentiment = sentiment['documents'][0]['score']
    print(sentiment)
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

def updateRefugee(id, text, sentiment, keywords, sentences):
    Migrant.objects.filter(pk=id).update(message_text=text, tags=keywords, sentiment=sentiment, excerpt=sentences)

def retrieveEntity(id):
    return Migrant.objects.filter(pk=id)

def retrieveEntityKeywords(keyword):
    return Migrant.objects.filter(tags__contains=keyword)

