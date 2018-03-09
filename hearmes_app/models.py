from django.db import models
import requests
import json
from pprint import pprint
from collections import namedtuple

#AZURE STUFF:
subscription_key="dac80f6bdc41438dbb9dcc1c9a81b3e1"
assert subscription_key
text_analytics_base_url = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0/"
language_api_url = text_analytics_base_url + "languages"
key_phrase_api_url = text_analytics_base_url + "keyPhrases"
sentiment_api_url = text_analytics_base_url + "sentiment"

#AZURE OCR TO TEXT:
ocr_subscription_key = "e3ce4c5f3d254832b89e0e0e996ecb8f"
assert ocr_subscription_key
ocr_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v1.0/"

# Create your models here.
#TODO: Model to upload document & details: Name, Birthdate, Document
class Migrant(models.Model):
    migrant_id = models.CharField(max_length=30,primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.CharField(max_length=3)
    profession = models.CharField(max_length=30)
    message = models.CharField(max_length=255, null=True)
    message_img_path = models.CharField(max_length=255, null=True)
    anonymity = models.CharField(max_length=30)

def uploadFormToDB(form_details):

    dump = json.dumps(form_details)
    data = json.loads(dump, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    p = Migrant(first_name=data.first_name, last_name=data.last_name, age = data.age , profession = data.profession, message = data.message, message_img = data.message_img, anonymity = data.anonymity)
    p.save()

    m = Migrant.objects.all()
    print(m)

    return 200

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

#TODO: Model for translation

#Model for sentiment and keywords detection
def analyzeDoc(doc):
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    sentiment_phrases_response = requests.post(sentiment_api_url, headers=headers, json=doc)
    key_phrases_response = requests.post(key_phrase_api_url, headers=headers, json=doc)
    key_phrases = key_phrases_response.json()
    sentiment_phrases = key_phrases_response.json()


#TODO: Model to get 2 sentences

#TODO: Model to upload to database

#TODO: Model to retrive from database based on tags