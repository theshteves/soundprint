import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView

from .forms import FileFieldForm, UploadFileForm
import decoder
import encoder


def api(request):

    response = {}
    if request.method == 'GET':

        # Return encoded message (soundprint)
        if request.GET.get('message'):
            response['soundprint'] = encoder.encode(request.GET['message'])

        # Return decoded message
        elif request.GET.get('soundprint'):
            response['message'] = decoder.decode(request.GET['soundprint'])

        else:
            response['error'] = 'missing 1 parameter (message or soundprint)'

    else:
        response['error'] = 'must send GET request'

    return HttpResponse(json.dumps(response, indent=4), \
                        content_type='application/json')


@csrf_protect
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            url = encoder.handle(request.FILES['file'])
            return HttpResponse(json.dumps({'soundprint': url}))

    else:
        form = UploadFileForm()

    return HttpResponse(json.dumps({'error': 'POST request form invalid',
                                    'form': str(form),
                                    'req': str(request.FILES)})) 
                                    #render(request, 'upload.html')

class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = '...'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
            	#url = encoder.handle(request.FILES['file'])
		pass
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def index(request):
    return render(request, 'index.html')

