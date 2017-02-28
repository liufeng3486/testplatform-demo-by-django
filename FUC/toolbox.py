# -*- coding: utf-8 -*-
import sys
from test1.models import Log
import random,datetime,urllib,urllib2,hashlib,time
import pylab
import os
import shutil
import requests
reload(sys)
sys.setdefaultencoding("utf-8")
def logInsert(url_src,data_src,type_src,name_src,res_src,poll_id,time_src,len_src):
    Log(poll =poll_id,
        url=url_src,
        data=data_src,
        type=type_src,
        name=name_src,
        response=res_src,
        response_len=len_src,
        response_time=time_src,
        ).save()

#这里处理random,time等特殊入参值

def dataManage(key,value):
    try: 
        temp = str(value).split('!.!')
        if temp[1]:
            data = ''
            if temp[0] == 'random':
                for i in range(int(temp[1])):
                    start = (1 if i==0 else 0)
                    data += str(random.randint(start,9))
                return data
            elif temp[0][:6] == 'random':
                if  temp[0][7:]=="letter":
                    data = randletter(temp[1],temp[2])
                elif temp[0][7:]=="int":
                    data = random.randint(int(temp[1]),int(temp[2]))
                else:
                    return False
                return data
            elif temp[0]== 'time':
                if temp[1]=='now':
                    data = str(datetime.datetime.now())
                return data
    except:
        return False
    return False




#将Request_Data object 转成 Dict 中间进行了!.!的处理,type是为了处理批量运行的问题
def requestDict(temp,type_="normal"):
    data = {}
    header={}
    if type_=="normal":
        for i in temp:
            # if i.key[:7].lower()=="header_":
            #     data[i.key[8:]]=i.value
            # else:
            data_temp = dataManage(i.key,i.value)
            if data_temp:
                data[str(i.key)]=data_temp
            else:
                data[str(i.key)]=(''if i.value=="null"else str(i.value))
    elif type_=="dict":
        for i in temp:
            data_temp = dataManage(i,temp[i])
            if data_temp:
                data[str(i)]=data_temp
            else:
                data[str(i)]=(''if temp[i]=="null"else str(temp[i]))
    else:
        for i in temp:
             data[str(i.key)]=(''if i.value=="null"else str(i.value))
    return data


#发送请求前做的数据处理，主要是进行加签
def reqGETDict(temp,type_="normal"):
    data_src = {}
    header_src ={}
    if type_ == "normal":
        for i in temp:
            if i[:7].lower()=="header_":
                header_src[i[7:]]=temp[i]
            if i != 'url' and i !='sign':
                data_src[i]=temp[i]
        data_src=signCreater(data_src,temp)
    else:
        for i in temp:
            if i[:7].lower()=="header_":
                header_src[i[7:]]=temp[i]
            elif i != 'url' and i !='TimesOfRepetition' and i !='VUserNum':
                data_src[i]=temp[i]
    return data_src,header_src

#这里用来判断是否需要加签，和进行加签API调用
def signCreater(data_src,temp):
    if "sign" in temp:#判断需要加签
        sign = signGet(temp['sign'].split("!.!"),data_src)
        if not sign:
            raise IOError,"Error Sign Data,Name!.!Type!.!Alg!.!Salt"
        else:
            data_src[sign[0]]=sign[1]
    else:
        pass
    return data_src

#给入字典和sign，根据sign的参数用来输出计算后的sign的key,value
def signGet(sign_rulls,src):
    salt = (None if len(sign_rulls)==3 else sign_rulls[3])
    if sign_rulls[1]=="null":#普通形式key=value&key=value……
        string = urllib.urlencode(src)
    elif sign_rulls[1] == "value":#只使用value, valuevalue……
        string = ''.join(src.values())+salt
    else:
        return False
    if sign_rulls[2] == "md5":#md5
        md5 = hashlib.md5()
        md5.update(string)
        value = md5.hexdigest()
    else:
        return False
    return sign_rulls[0],value

#数字转换为字母
def num_letter(b,list):
    if b>51:
        list.append(b%52)
        return num_letter(b/52,list)
    else:
        list.append(b)
        list.reverse()
        letter=""
        for i in list:
            i = (chr(i+97) if i<26 else chr(i+39))
            letter += i
        return letter

#字母转换为数字
def letter_num(data):
    list = []
    for i in data:
        temp = (ord(i)-39 if i<'a' else ord(i)-97)
        list.append(temp)
    sum = 0
    for i,j in enumerate(list):
        if sum ==0 and j==0:
            sum+= 1*(52**(len(list)-1-i))
        else:
            sum += j*(52**(len(list)-1-i))
    return list,sum

#获取字母随机数
def randletter(start,end):
    try:
        start = letter_num(start)[1]
        end =  letter_num(end)[1]
        return num_letter(random.randint(start,end),[])
    except Exception,e:
        print Exception,":",e
        print "error start or end need a-Z"

#批量接口执行
def post_more(url,data_list,time=1,res_list=[]):
    start = 0
    for j in range(time):
        for i in data_list:
            res = post_normal(url,i)
            if res_list[3].acquire(1):#这是个线程锁
                if start == 0:start=res[2]
                if res[0] :
                    res_list[0] += 1#ok += 1
                    res_list.append([1,res[1],round(res[2]-start,3),round(res[3],3)])#记录:  状态，数据量，起始时间，耗时
                else:
                    res_list[1] += 1#error += 1
                    res_list.append([0,res[1],round(res[2]-start,3),round(res[3],3)])
                res_list[2] += res[1]
                res_list[3].release()
    return res_list#ok,error,sum_res,

#入参为DICT，  return 结果，数据长度，开始时间，用时
def post_normal(url,data):
    start = time.time()
    try:
        url2 = urllib2.Request(url,data)
        response = urllib2.urlopen(url2)
        end = time.time()-start
        apicontent = response.read()
        #这里要做个结果判断的
        return True,len(apicontent),start,end
    except:
        return False,0,start,0


#绘图前的数据准备，入口数据样式a= [[1, 49460, 0.0, 1.751], [1, 49460, 1.891, 0.53],[执行结果，返回长度，起始时间，耗时]
def  drawDateReady(data_src):
    b = [];pass_temp_list = [0];error_temp_list = [0];time_temp_list = [0];data_temp_list = [0] #定义分数据数组
    for i in data_src:b.append([i[0],i[1],i[2]+i[3]]) #组合请求时间
    b.sort(key = lambda x:x[2]) #排序
    for i in b:
        time_temp_list.append(i[2]) #时间数组添加成员
        data_temp_list.append(data_temp_list[-1]+i[1]) #数据长度数组添加成员
        pass_temp = 1;error_temp = 1 #定义执行情况
        if i[0]==1:error_temp = 0 #判断执行情况
        else:pass_temp = 0
        pass_temp_list.append(pass_temp_list[-1]+pass_temp) #统计执行结果
        error_temp_list.append(error_temp_list[-1]+error_temp)
    result_range = [0,int(b[-1][-1]*1.02+1),-1,int(len(b)*1.02+1)]
    datalen_range = [0,int(b[-1][-1])+1,int(-1*(data_temp_list[-1])*0.02),int(data_temp_list[-1]*1.02)]
    return [pass_temp_list,error_temp_list],data_temp_list,time_temp_list,result_range,datalen_range #结果统计LIST,数据统计LIST，时间轴，结果统计范围，数据长度范围

#这个数据整理后，用来给highchar使用
def hcharDateReady(data_src):
    pass_list =[]
    error_list=[]
    data_list=[]
    for i in range(len(data_src[2])):
        pass_list.append([data_src[2][i],data_src[0][0][i],])
        error_list.append([data_src[2][i],data_src[0][1][i],])
        data_list.append([data_src[2][i],data_src[1][i],])
    return pass_list,error_list,data_list,data_src[3],data_src[4]



#执行结果图表绘制
def drawChart_Xs(y_list,x_list,showrange,name):
    pylab.axis(showrange)
    pylab.plot(x_list, y_list[0],'g*', linewidth=2.0)
    pylab.plot(x_list, y_list[1],'r*', linewidth=2.0)
    pylab.xlabel('time(s)')
    pylab.ylabel('num')
    pylab.title('Statistical of Result')
    pylab.grid(True)
    pylab.savefig(name)
#总数据量图表绘制
def drawChart_X(y_list,x_list,showrange,name):
    pylab.axis(showrange)
    pylab.plot(x_list, y_list,'g*', linewidth=2.0)
    pylab.xlabel('time(s)')
    pylab.ylabel('len')
    pylab.title('Amount of data statistics')
    pylab.grid(True)
    pylab.savefig(name)

class FileGod():
    def removeFileInFirstDir(self,targetDir):
        for file in os.listdir(targetDir):
            targetFile = os.path.join(targetDir,  file)
            if os.path.isfile(targetFile):
                os.remove(targetFile)

    #获取目录下的PY文件list
    def getPyList(self,file_list):
        py_list = []
        for i in file_list:
            temp = i.split(".")
            if len(temp)>1 and temp[1]=="py" and temp[0]!="__init__" and temp[0]!="casetemplate":
                py_list.append(temp[0])
        return py_list
    #获取目录下TXT文件LIST
    def getLogList(self,file_list,src_list):
        log_list =[]
        print src_list
        for i in src_list:
            if i+".txt" in file_list:
                log_list.append(i)
        if "all.txt" in file_list:
            log_list.append("all")
        return log_list


#给dtree返回文件列表 a = dtreeList(path); list=a.getlist()
class dtreeList():
    def __init__(self,path,goal_path="./TestCasePro/RUNCASE/"):
        self.goal_path = goal_path
        self.path=path
        self.dtree_list =[];self.c_dirc = {}
        self.s_num=0;self.c_num=0
    def run(self,path,f_num):
        if self.s_num ==0:
            self.dtree_list.append([self.s_num,-1,"CASE","",""])
        else:
            temp = path.replace('\\','/')#统一路径格式
            self.dtree_list.append([self.s_num,f_num,"authority","",temp.split('/')[-1]])#只显示文件夹名称
        f_num = self.s_num
        self.s_num +=1
        a =  os.listdir(path)
        for i in a:
            full_file_name = os.path.join(path, i)
            if os.path.isdir(full_file_name):
                self.run(full_file_name,f_num)
            elif i.split(".")[0][:1]!="_" and i.split(".")[1]=="py" and i.split(".")[0]!="casetemplate":
                self.dtree_list.append([self.s_num,f_num,"authority",self.c_num,i])
                self.c_dirc[self.c_num]=full_file_name.replace('\\','/')
                self.s_num+=1
                self.c_num+=1
    def pycopy(self,casedirc):
        try:
            shutil.copy('./TestCasePro/CASE/__init__.py',self.goal_path) #复制init
            shutil.copy('./TestCasePro/CASE/casetemplate.py',self.goal_path) #复制用例模板文件
            for i in casedirc:
                shutil.copy(casedirc[i],self.goal_path+casedirc[i][19:].replace('/','_'))#修改文件名并复制
            return True
        except:
            return False

    def getlist(self):
        self.run(self.path,0)
        return self.dtree_list,self.c_dirc


#编码相关class ，转码方法以“coding_”开头
class CodeGod():
    def __init__(self,data):
        self.data = data
        from collections import OrderedDict
        self.req_dict=OrderedDict()
    #批量执行coding函数
    def code_try(self):
        temp_function_list = dir(self)
        first = self.code_first(self.data)
        self.req_dict[first[0]]=first[1]
        for i in temp_function_list:
            if i[:7]=="coding_" :
                temp = eval("self.%s(self.data)"%i)
                self.req_dict[i[7:]]=(temp if temp else "None")
        return self.req_dict
    #16进制转utf8
    def coding_ffToUtf(self,data):
        try:
            string=''
            for i in range(0,len(data),2):
                string += chr((int(data[i],16)<<4)+int(data[i+1],16))
            return string
        except:
            return False
    def code_first(self,data):
        import chardet
        try:
            temp = chardet.detect(str(data))
            return str(temp['confidence']*100)+"%",temp['encoding']
        except:
            return "0%","False"



# # 合并入 File God
# #获取目录下的PY文件list
# def getPyList(file_list):
#     py_list = []
#     for i in file_list:
#         temp = i.split(".")
#         if len(temp)>1 and temp[1]=="py" and temp[0]!="__init__" and temp[0]!="casetemplate":
#             py_list.append(temp[0])
#     return py_list
#
# #获取目录下TXT文件LIST
# def getLogList(file_list,src_list):
#     log_list =[]
#     print src_list
#     for i in src_list:
#         if i+".txt" in file_list:
#             log_list.append(i)
#     if "all.txt" in file_list:
#         log_list.append("all")
#     return log_list