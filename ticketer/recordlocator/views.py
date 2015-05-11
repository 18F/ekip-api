import json

from django.shortcuts import render
from django.http import HttpResponse

from recordlocator import generator

def record_locators(request):

    record_locator = generator.safe_generate()
    response = {'record_locators': [record_locator]}
    data = json.dumps(response)

    return HttpResponse(data, content_type='application/json')
