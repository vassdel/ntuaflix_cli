from django.template import loader
from django.http import HttpResponse

def cli(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())