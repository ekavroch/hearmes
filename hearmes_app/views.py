from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, View
import requests
import datetime
import json
from django.http import JsonResponse
from hearmes_app import models

# Create your views here.
##TODO: Create view of an article

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm

class showStory(View):
    #load the whole story
    template_name = 'story.html'
    def get(self, request):
        refugee = models.retrieveEntity(request.GET.get('ref_id'))
        print(refugee)
        return render(request, self.template_name, refugee)

class searchQuotes(CreateView):
    template_name = 'search.html'
    form_class = UserCreationForm

class searchKeywords(View):
    template_name = 'results.html'
    def get(self, request):
        ads = models.retrieveEntityKeywords(request.GET.get('keyword'))
        print(ads)


def registerRefugee(request):
    #Prepare data:
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    destination = request.POST.get('destination')
    age = request.POST.get('age')
    job = request.POST.get('job')
    tags = ""
    date = str(datetime.datetime.now())
    story_url = ""

    #Upload the story
    if request.method == 'POST' and request.FILES['story']:
        myfile = request.FILES['story']
        fs = FileSystemStorage()
        filename = fs.save('stories/'+first_name + '_story.jpg', myfile)
        story_url = fs.url(filename)

    #JSON:
    refugee = {
        "first_name":first_name,
        "last_name":last_name,
        "destination":destination,
        "age":age,
        "story_url":story_url,
        "job":job,
        "tags":tags,
        "date":date
    }


    #Send to DB:
    savedRefugee = models.uploadFormToDB(refugee)
    text = models.JPEGtoText(story_url)
    keywords, sentiment = models.analyzeStory(text)
    models.updateRefugee(savedRefugee.migrant_id, text, sentiment, keywords)

    data = {
        'res': 200,
    }

    return JsonResponse(data)





