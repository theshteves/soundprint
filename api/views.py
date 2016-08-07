import json

from django.shortcuts import render
from django.http import HttpResponse

import tool


def api(request):

    response = {}
    if request.method == 'GET':

        # Return encoded message (soundprint)
        if request.GET.get('message'):
            response['soundprint'] = tool.encode(request.GET['message'])

        # Return decoded message
        elif request.GET.get('soundprint'):
            response['message'] = tool.decode(request.GET['soundprint'])

        else:
            response['error'] = 'missing 1 parameter (message or soundprint)'

    else:
        response['error'] = 'must send GET request'

    return HttpResponse(json.dumps(response, indent=4), \
                        content_type='application/json')


def index(request):
    return render(request, 'index.html')

