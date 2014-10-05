from django.db import models

# Create your models here.
class Company(models.Model):
    
    def __unicode__(self):
        return self.name
 	class Meta:
 		verbose_name_plural =_('Companies')
    name = models.CharField(max_length=50)
    # application_deadline = models.DateField()

class Contact(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50)
    phone_number = models.IntegerField(default=0)
    # email = models.CharField(max_length=50)
    # employer = models.CharField(max_length=50)


class Event(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50)
    date = models.DateField()


class Profile(models.Model):
	def __unicode__(self):
		return self.name

	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(max_length=60)
	phone_number = models.IntegerField(default=0)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=40)
	state = models.CharField(max_length=13)
	zip_code = models.CharField(max_length=6)

	#An error may occur here, unsure as to what rep of radiobutton is
	gender = models.CharField(max_length=10)

	school = models.CharField(max_length=50)

	grad_month = models.CharField(max_length=10)
	grad_year = models.IntegerField(default = 0000, max_length=5)