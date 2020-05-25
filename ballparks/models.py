from django.db import models

class Ballpark(models.Model):
	name = models.CharField(max_length=255)
	team = models.CharField(max_length=255)
	league = models.CharField(max_length=255)
	latitude = models.DecimalField()
	longitude = models.DecimalField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)