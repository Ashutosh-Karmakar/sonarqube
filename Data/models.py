from tkinter import CASCADE
from django.db import models
from django.conf import settings

class Names(models.Model): #Names is the new database which extends to models.Model 
    #here we can create new database just without using sql query
    #we can see this in migration
    name = models.CharField(max_length=100) 
    age = models.IntegerField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) #foreign key to NewUser model 
