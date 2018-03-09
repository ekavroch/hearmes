from django.db import models
import requests
from collections import namedtuple
import json
import urllib.parse

#AZURE OCR TO TEXT:
ocr_subscription_key = "e3ce4c5f3d254832b89e0e0e996ecb8f"
assert ocr_subscription_key
ocr_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v1.0/"


# Create your models here.
#TODO: Model to upload document & details: Name, Birthdate, Document
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthdate = models.CharField(max_length=30)
    occupation = models.CharField(max_length=30)
    message = models.CharField(max_length=30)

def uploadFormToDB(form_details):

    dump = json.dumps(form_details)
    data = json.loads(dump, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


    print(data.first_name)
    #Save to database. Check datase content


#TODO: Model to change JPG to Computer Text
def JPEGtoText():
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Cursive_Writing_on_Notebook_paper.jpg/800px-Cursive_Writing_on_Notebook_paper.jpg"

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

    for line in analysis["recognitionResult"]["lines"]:
        print(line['text'])

#Model for transalation
def transalte (target, text):
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

#TODO: Model to upload to database

#TODO: Model to retrive from database based on tags