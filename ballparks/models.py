from django.db import models

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)

class Ballpark(models.Model):
	name = models.CharField(max_length=255)
	team = models.CharField(max_length=255)
	league = models.CharField(max_length=255)
	latitude = models.DecimalField(decimal_places=3, max_digits=8)
	longitude = models.DecimalField(decimal_places=3, max_digits=8)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)