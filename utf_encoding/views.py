from django.shortcuts import render
from django.http import HttpResponse
from FUC.toolbox import *
import json
# Create your views here.
#def index(req):
 #   return render(req,'utf_encoding\index.html')


def index(request):
    return render(request, 'utf_encoding\index.html')
    
def add(request):
    string=''
    data = request.GET['a']
    for i in range(0,len(data),2):
        string += chr((int(data[i],16)<<4)+int(data[i+1],16))
    return HttpResponse(string)

# def ff_2_UTF(data):
#     string=''
#     for i in range(0,len(data),2):
#         string += chr((int(data[i],16)<<4)+int(data[i+1],16))
#     return string


def deUncode(request):
    data = request.GET['src']
    code_human = CodeGod(data)
    code_dict = code_human.code_try()
    json_data = json.dumps(code_dict)
    return HttpResponse(json_data)




