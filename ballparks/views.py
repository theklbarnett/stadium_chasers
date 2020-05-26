from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

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
			return redirect('/signin')
		else:
			request.session['first_name'] = User.objects.get(email=request.POST['email_login']).first_name
			request.session['logged_on'] = True
			request.session['user_id'] = User.objects.get(email=request.POST['email_login']).id
			request.session['user_level'] = User.objects.get(email=request.POST['email_login']).user_level
			return redirect('/dashboard')

def register_user(request):
	if request.method == "POST":
		errors = User.objects.registration_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value, extra_tags="register")
			return redirect('/register')
		else:
			if (len(User.objects.all()) < 1):
				User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], birthday=request.POST['birthday'], email=request.POST['email'], user_level=9, password_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode())
			else:
				User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], birthday=request.POST['birthday'], email=request.POST['email'], password_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode())
			if request.session.get('logged_on', False) == False:
				request.session['first_name'] = User.objects.get(email=request.POST['email']).first_name
				request.session['user_id'] = User.objects.get(email=request.POST['email']).id
				request.session['logged_on'] = True
				request.session['user_level'] = User.objects.get(email=request.POST['email']).user_level
			return redirect("/dashboard")