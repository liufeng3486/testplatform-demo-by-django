from django.contrib import admin

# Register your models here.
from test1 import models as test1_models

# admin.site.register(test1_models.Person)

# class ChoiceInline(admin.StackedInline):
#     model=polls_models.Choice
#     extra=3
class Data_list(admin.StackedInline):
    model=test1_models.Request_Data
    #extra=3


class Test1Admin(admin.ModelAdmin):
    fields = ['url','data','type','name']
    inlines = [Data_list]




admin.site.register(test1_models.Request,Test1Admin)

admin.site.register(test1_models.Log)
