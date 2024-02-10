from django.template import loader
from django.http import JsonResponse
from django.http import HttpResponse
import json

def cli(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())
    

def user_endpoint_view(request):
    filepath = 'user.json'
    with open(filepath, 'r') as file:
        data = json.load(file)
    # Return JSON response
    return JsonResponse(data, safe=False)