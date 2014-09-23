from django.db import models

# Create your models here.
class Company(models.Model):
    
    def __unicode__(self):
        return self.name
    
    name = models.CharField(max_length=50)

class Contact(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50)
    phone_number = models.IntegerField(default=0)
