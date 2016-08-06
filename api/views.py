from django.shortcuts import render
from django.http import HttpResponse

# POST request
def decode(request):
    
    # Accept audio & return text
    return HttpResponse('decoding...')


# POST request
def encode(request):

    # Accept text & return audio
    return HttpResponse('encoding...')


# GET request
def index(request):
    return render(request, 'index.html')

