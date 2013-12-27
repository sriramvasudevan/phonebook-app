from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

     
class Contact(models.Model):
    user=models.ManyToManyField(User)
    name=models.CharField(max_length=200)
    ph_no=models.BigIntegerField(null=True, blank=True)
    email=models.EmailField(max_length=200, null=True, blank=True)
    timestamp=models.DateTimeField(null=True, blank=True)
        
    def __unicode__(self):
        return self.name
                
    class Meta:
        ordering = ['name']
