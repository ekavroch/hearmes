from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
import requests
import datetime
import json
from hearmes_app import models

# Create your views here.
##TODO: Create view of an article

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm

def registerRefugee(request):
    #Prepare data:
    first_name = request.GET.get('first_name', None)
    last_name = request.GET.get('last_name', None)
    destination = request.GET.get('destination', None)
    age = requests.GET.get('age', None)
    story = requests.GET.get('story', None)
    job = requests.GET.get('job', None)
    tags = requests.GET.get('tags', None)
    date = datetime.datetime.now()

    #JSON:
    refugee = {
        "first_name":first_name,
        "last_name":last_name,
        "destination":destination,
        "age":age,
        "story":story,
        "job":job,
        "tags":tags,
        "date":date
    }

    #Send to DB:
    res = models.uploadFormToDB(refugee)
    return res





