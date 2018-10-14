from django.db import models

# Create your models here.

class Person(models.Model):
	name = models.CharField(max_length=100)
	age = models.IntegerField()
	parentContactNumber = models.CharField(max_length=10, verbose_name="Parent's Contact Number")
	address = models.TextField()
	height = models.CharField(verbose_name="Height (CM)", max_length=100)
	weight = models.CharField(verbose_name="Weight (KG)", max_length=100)
	about = models.TextField(null=True, blank=True)
	date_of_missing = models.DateField(blank=True, null=True)
	place_of_missing = models.CharField(max_length=100, blank=True, null=True)
	is_missing = models.BooleanField(default=True)
	image = models.ImageField()
	created = models.DateTimeField(auto_now_add=True)

	
	def __str__(self):
		return self.name