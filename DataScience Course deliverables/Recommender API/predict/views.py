# from data import predictions.json
import json
import os
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request, userID):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'predictions.json')

    with open(file_path) as file:
        for line in file:
            record = json.loads(line)
            try:
                if userID in record.keys():
                    return HttpResponse(record.values())
            except:
                pass
        
        return HttpResponse("NOT FOUND")