from django.db import models
import requests
import urllib.parse
# Create your models here.

#TODO: Model to upload document & details

#TODO: Model to change JPG to Computer Text

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