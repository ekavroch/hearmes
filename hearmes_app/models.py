from django.db import models
import requests
from pprint import pprint

#AZURE STUFF:
subscription_key="dac80f6bdc41438dbb9dcc1c9a81b3e1"
assert subscription_key
text_analytics_base_url = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0/"
language_api_url = text_analytics_base_url + "languages"
key_phrase_api_url = text_analytics_base_url + "keyPhrases"
sentiment_api_url = text_analytics_base_url + "sentiment"




# Create your models here.

#TODO: Model to upload document & details

#TODO: Model to change JPG to Computer Text

#TODO: Model for transalation

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