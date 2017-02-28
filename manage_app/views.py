from django.shortcuts import render

# Create your views here.

def index(req):
    # Request_List = Request.objects.all()
    context = {'Request_List':"ddddd"}
    return render(req,'index.html',context)