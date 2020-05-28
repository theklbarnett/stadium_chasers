from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
	def registration_validator(self, post_data):
		errors = {}
		email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if len(post_data['first_name']) < 2:
			errors['first_name'] = "First name must be at least 2 characters"
		if len(post_data['last_name']) < 2:
			errors['last_name'] = "Last name must be at least 2 characters"
		if not email_regex.match(post_data['email']):
			errors['email'] = "Invalid email address"
		if User.objects.filter(email=post_data['email']):
			errors['unique'] = "Email address already exists"
		if len(post_data['password']) < 8:
			errors['password'] = "Password must be at least 8 characters"
		if post_data['password'] != post_data['confirm_password']:
			errors['confirm_password'] = "Passwords did not match"
		return errors

	def authentication_validator(self, post_data):
		errors = {}
		if User.objects.filter(email=post_data['email']):
			if not bcrypt.checkpw(post_data['password'].encode(), User.objects.get(email=post_data['email']).password_hash.encode()):
				errors['password'] = "Incorrect password"
		else:
			errors['email'] = 'This email does not exist'
		return errors
		
class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password_hash = models.CharField(max_length=60)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Ballpark(models.Model):
	team = models.CharField(max_length=255)
	visited = models.BooleanField()
	users = models.ManyToManyField(User, related_name='ballparks')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)