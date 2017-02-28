from django.shortcuts import render
from django.http import HttpResponse
import hashlib,json

# Create your views here.

def index(request):
    return render(request, 'md5_encoding\index.html')
    
def md5(request):
    req_dict={}
    data = request.GET['pass']
    salt = request.GET['salt']
    m = hashlib.md5()
    m_2 = m
    m.update(data)
    req_dict["md5($pass)"]=m.hexdigest()
    m_2.update(req_dict["md5($pass)"])
    req_dict["md5(md5($pass))"]=m_2.hexdigest()
    json_data = json.dumps(req_dict)
    #return HttpResponse(m.hexdigest())
    return HttpResponse(json_data)


