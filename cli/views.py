from django.template import loader
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

def cli(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())
    

@csrf_exempt  # Disable CSRF token for this example. Use cautiously.
@require_http_methods(["POST"])  # Ensure that only POST requests are accepted.
def user_endpoint_view(request):
    try:
        # Parse the JSON data from request body
        data = json.loads(request.body)
        
        # Example: Process the data as needed
        username = data.get('username')
        password = data.get('password')
        # Add your logic here to handle the username and password or any other data
        
        return JsonResponse({'message': 'Data processed successfully', 'data': data})
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')
    except KeyError:
        # Handle missing keys if necessary
        return HttpResponseBadRequest('Missing required data')