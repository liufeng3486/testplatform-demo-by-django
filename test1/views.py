# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.shortcuts import render,render_to_response
from test1.models import Person,Request,Log,Request_Data
from FUC import toolbox
from django.http import HttpResponse
import datetime,copy,time,threading

import urllib2,urllib,hashlib
# Create your views here.

def index(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'test1/index.html',context)

def indexPost(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'test1/indexPost.html',context)

def indexGet(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'test1/indexGet.html',context)

def indexGetBatch(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'test1/indexGetBatch.html',context)

def indexPostBatch(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'test1/indexPostBatch.html',context)

#post相关
def post_ready(req,test1_id):
    prc = Request.objects.get(id=test1_id)
    temp = Request_Data.objects.filter(f_key=test1_id)
    data = toolbox.requestDict(temp)
    context = {'url':prc.url,'data':data,'name':prc.name}
    return render(req,'test1/post_sub.html',context)
def post_batch_ready(req,test1_id):
    prc = Request.objects.get(id=test1_id)
    temp = Request_Data.objects.filter(f_key=test1_id)
    data = toolbox.requestDict(temp,"batch")#不进行数据预处理
    context = {'url':prc.url,'data':data,'name':prc.name}
    return render(req,'test1/post_batch_sub.html',context)

def post_ok(req,test1_id):
    data_src=toolbox.reqGETDict(req.GET)[0]
    header_src =toolbox.reqGETDict(req.GET)[1]
    data = urllib.urlencode(data_src)
    start = time.time()
    url2 = urllib2.Request(req.GET['url'],data)
    # for i in header_src: #头文件更改
    #     url2.add_header(i,header_src[i])
    print data_src,header_src,data
    response = urllib2.urlopen(url2)
    apicontent = response.read()    
    toolbox.logInsert(req.GET['url'],data_src,'POST',
               Request.objects.get(id=test1_id).name,apicontent,
               Request.objects.get(id=test1_id),str(time.time()-start),str(len(apicontent)))
    return HttpResponse(apicontent)

#入参为多条请求组合的LIST， return 正确，失败，总长度，时间LIST


#发一群POST
def post_batch_ok(req,test1_id):
    data_src=toolbox.reqGETDict(req.GET,"no normal")[0]#页面内容转为字典，直接DICT会造成u''的问题 后面的参数是为了暂缓进行加签
    TimesOfRepetition = int(req.GET['TimesOfRepetition']) #获取次数
    VUserNum = int(req.GET['VUserNum'])
    start = time.time()
    data_list=[]
    res_list=[0,0,0,threading.Lock()]
    for i in range(TimesOfRepetition):
        data = toolbox.requestDict(data_src,"dict") #进行数据整理 !.!类型数据生成
        # data = toolbox.signCreater(data,{'sign':req.GET['sign']}) #进行加签操作
        data = urllib.urlencode(data)#GET拼接
        data_list.append(data)
    threads = []
    if VUserNum==1:#单一用户就发一组
        toolbox.post_more(req.GET['url'],data_list,1,res_list)
    else:#发N组
        for i in range(VUserNum):
            exec "t%d = threading.Thread(target=toolbox.post_more,args=(req.GET['url'],data_list,1,res_list))"%i
            exec "threads.append(t%d)"%i
        for t in threads:
            t.setDaemon(True)
            t.start()
            t.join()
        time.sleep(1)#有可能丢包，再说
    end = time.time()-start
    #以下内容是通过pylab生成image后，再显示到页面
    #绘图
    # nowtime = datetime.datetime.now().strftime("%Y-%m-%d%H%M%S")
    # res = toolbox.drawDateReady(res_list[4:])
    # toolbox.drawChart_Xs(res[0],res[2],res[3],'static/png/'+nowtime+'Result')
    # toolbox.drawChart_X(res[1],res[2],res[4],'static/png/'+nowtime+'Amountofdata')
    #
    #记LOG
    # toolbox.logInsert(req.GET['url'],res_list[4:],'POST', #URL，DATA,TYPE
    #                   Request.objects.get(id=test1_id).name,str(res_list[2]), #NAME
    #                   Request.objects.get(id=test1_id),str(end),str("pass:"+str(res_list[0])+" error:"+str(res_list[1])))#RESPONSE,LEN,TIME
    # #return HttpResponse("pass:"+str(res_list[0])+" error:"+str(res_list[1]),'1')#"pass:"+str(ok)+" error:"+str(error)
    # context={'res':"pass:"+str(res_list[0])+" error:"+str(res_list[1]),'imgs':['/static/png/'+nowtime+'Result.png','/static/png/'+nowtime+'Amountofdata.png']}
    # return render(req,'test1/showBatchRes.html',context)
    #这里是通过highchar生成动态图表
    Requset_list = toolbox.drawDateReady(res_list[4:])
    Requset_list = toolbox.hcharDateReady(Requset_list)
    context = {'pass_list':Requset_list[0],'error_list':Requset_list[1],'data_list':Requset_list[2],'rang_1':Requset_list[3],'rang_2':Requset_list[4]}
    return render(req,'test1/showBatchRes.html',context)

#get相关
def get_ready(req,test1_id):
    prc = Request.objects.get(id=test1_id)
    temp = Request_Data.objects.filter(f_key=test1_id)
    temp = toolbox.requestDict(temp)
    data = temp[0]
    header = temp[1]
    context = {'url':prc.url,'data':data,'name':prc.name}   
    return render(req,'test1/post_sub.html',context)
def get_batch_ready(req,test1_id):
    prc = Request.objects.get(id=test1_id)
    temp = Request_Data.objects.filter(f_key=test1_id)
    data = toolbox.requestDict(temp,"batch")#不进行数据预处理
    context = {'url':prc.url,'data':data,'name':prc.name}
    return render(req,'test1/get_batch_sub.html',context)
def get_ok(req,test1_id):
    data_src=toolbox.reqGETDict(req.GET)[0]#页面内容转为字典，直接DICT会造成u''的问题
    data = urllib.urlencode(data_src)#GET拼接
    url = req.GET['url']+"?"+data
    start = time.time()
    req_temp = urllib2.Request(url)
    res_data = urllib2.urlopen(req_temp)
    end = time.time()-start
    res = res_data.read()
    toolbox.logInsert(req.GET['url'],url.split('?')[1],'GET',
                      Request.objects.get(id=test1_id).name,res,
                      Request.objects.get(id=test1_id),str(end),str(len(res)))
    return HttpResponse(res)
def get_batch_ok(req,test1_id):
    data_src=toolbox.reqGETDict(req.GET,"no normal")[0]#页面内容转为字典，直接DICT会造成u''的问题 后面的参数是为了暂缓进行加签
    TimesOfRepetition = req.GET['TimesOfRepetition'] #获取次数
    VUserNum = req.GET['VUserNum']
    ok=error=sum_res=0
    start = time.time()
    for i in range(int(TimesOfRepetition)):
        data = toolbox.requestDict(data_src,"dict") #进行数据整理 !.!类型数据生成
        data = toolbox.signCreater(data,{'sign':req.GET['sign']}) #进行加签操作
        data = urllib.urlencode(data)#GET拼接
        url = req.GET['url']+"?"+data
        try:
            req_temp = urllib2.Request(url)
            res_data = urllib2.urlopen(req_temp)
            res = res_data.read()
            sum_res += len(res)
            ok +=1
            #这里要做个结果判断的
        except:
            error +=1
    end = time.time()-start
    toolbox.logInsert(req.GET['url'],str(TimesOfRepetition),'GET',
                      Request.objects.get(id=test1_id).name,str(sum_res),
                      Request.objects.get(id=test1_id),str(end),str("pass:"+str(ok)+" error:"+str(error)))
    return HttpResponse("pass:"+str(ok)+" error:"+str(error))






def get_title():
    person_list = Person.objects.all()
    print person_list


