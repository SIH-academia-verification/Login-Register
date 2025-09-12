
from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,default="")
    phone = models.TextField(default="")
    # password = models.CharField(max_length=50,default="")
    date = models.DateField(default=date.today)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    certificate_hash = models.CharField(max_length=64, blank=True, null=True) 
    
    def __str__(self):
        return self.name


