from django.db import models

# Create your models here.

class Person(models.Model):
	name = models.CharField(max_length=100)
	age = models.IntegerField()
	fathersName = models.CharField(max_length=100)
	parentContactNumber = models.CharField(max_length=10, verbose_name="Parent's Contact Number")
	address = models.TextField()
	nearest_police_station = models.CharField(max_length=100)
	height = models.CharField(verbose_name="Height (CM)", max_length=100)
	weight = models.CharField(verbose_name="Weight (KG)", max_length=100)
	complexion = models.CharField(max_length=100)
	date_of_missing = models.DateField(blank=True, null=True)
	place_of_missing = models.CharField(max_length=100, blank=True, null=True)
	is_missing = models.BooleanField(default=True)
	image = models.ImageField(null=True, blank= True)
	created = models.DateTimeField(auto_now_add=True)

	
	def __str__(self):
		return self.name