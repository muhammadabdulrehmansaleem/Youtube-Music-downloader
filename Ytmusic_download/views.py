# Ytmusic_download/Ytmusic_download/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Ytmusic_download app!")
