from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
import datetime
import json

# Create your views here.
##TODO: Create view of an article

def current_datetime(request):
    now = datetime.datetime.now()
    t = get_template('test.html')
    html = t.render({'current_date': now})
    return HttpResponse(html)

##TODO: Create view of 2 sentences

##TODO: Create view of registration page

#TEST
def ocr_test_site():
    now = datetime.datetime.now()
    t = get_template('ocr_test.html')
    html = t.render({'current_date': now})  #var:value
    return HttpResponse(html)