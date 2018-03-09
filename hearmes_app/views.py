from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
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

def registerRefugee(request):
    #Prepare data:
    print(request.POST.get('first_name'))
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    destination = request.POST.get('destination')
    age = request.POST.get('age')
    job = request.POST.get('job')
    tags = request.POST.get('tags')
    date = datetime.datetime.now()
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
        "story":story_url,
        "job":job,
        "tags":tags,
        "date":date
    }


    #Send to DB:
    savedRefugee = models.uploadFormToDB(refugee)
    text = models.JPEGtoText(story_url)
    model.updateDB(savedRefugee.id,"story_text", text)

    data = {
        'res': 200,
    }

    return JsonResponse(data)





