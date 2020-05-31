from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from django.http import JsonResponse
from .models import User, Ballpark


def login_user(request):
	return render(request, 'login.html')


def homepage(request):
	return render(request, 'homepage.html')


def render_park(request):
	pass

# Functions associated with LOGIN and REGISTER:


def authenticate_user(request):
	if request.method == "POST":
		errors = User.objects.authentication_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value, extra_tags='login')
			return redirect('/')
		else:
			request.session['first_name'] = User.objects.get(
			    email=request.POST['email']).first_name
			request.session['logged_on'] = True
			request.session['user_id'] = User.objects.get(
			    email=request.POST['email']).id
			return redirect('/home')


def register_user(request):
	if request.method == "POST":
		errors = User.objects.registration_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value, extra_tags="register")
			return redirect('/')
		else:
			User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],
			                    password_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode())
			if request.session.get('logged_on', False) == False:
				request.session['first_name'] = User.objects.get(
				    email=request.POST['email']).first_name
				request.session['user_id'] = User.objects.get(
				    email=request.POST['email']).id
				request.session['logged_on'] = True
			return redirect("/home")


def stadium_info(request):
	return render (request, 'stadiums.html')

def national_stadiums(request):
	return render (request, 'national.html')


def tracker(request):
	return render (request, 'tracker.html')

def bucket (request):
	context = {
		'stadiums': Ballpark.objects.filter(user=User.objects.get(id=request.session['user_id']))
	}
	return render (request, 'bucket.html', context)


def logout(request):

	request.session.flush()

	return redirect('/')

def bucket_add(request):
	team = request.GET.get('team', None).replace('-', ' ')
	Ballpark.objects.create(team=team, visited=False, user=User.objects.get(id=request.session['user_id']))
	data = {
		'complete': True
	}
	return JsonResponse(data)

def bucket_remove(request, id):
	c = Ballpark.objects.get(id=id)
	c.delete()
	return redirect('/bucket')

def bucket_visit(request, id):
	c = Ballpark.objects.get(id=id)
	c.visited = True
	c.save()
	return redirect('/bucket')

def bucket_visited_at(request, id):
	c = Ballpark.objects.get(id=id)
	c.visited_at = request.POST['visited_at']
	c.save()
	return redirect('/bucket')
