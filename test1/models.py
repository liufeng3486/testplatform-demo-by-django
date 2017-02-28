from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Person(models.Model):
    person_name = models.CharField(max_length=200)
    person_create_date = models.DateTimeField()
    person_age  = models.IntegerField()
    person_other = models.CharField(max_length=200)


class Request(models.Model):
    url = models.CharField(max_length=200,null=True)
    data = models.CharField(max_length=1000,null=True)
    type = models.CharField(max_length=50,null=True)
    name = models.CharField(max_length=50,null=True)
    def __unicode__(self):
        return self.name

class Log(models.Model):
    poll = models.ForeignKey(Request,null=True)
    url = models.CharField(max_length=200,null=True)
    data = models.CharField(max_length=1000,null=True)
    type = models.CharField(max_length=50,null=True)
    name = models.CharField(max_length=50,null=True)
    create_time = models.DateTimeField(auto_now=True)
    response = models.CharField(max_length=1000,null=True)
    response_len = models.CharField(max_length=20,null=True)
    response_time = models.CharField(max_length=20,null=True)
    def __unicode__(self):
        return str(self.create_time)

class Request_Data(models.Model):
    f_key = models.ForeignKey(Request,null=True)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=1000,null=True)
    
