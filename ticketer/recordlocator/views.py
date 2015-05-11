import json

from django.shortcuts import render
from django.http import HttpResponse

def record_locators(request):
    response = {'record_locators': ['XYg112']}
    data = json.dumps(response)

    return HttpResponse(data, content_type='application/json')
