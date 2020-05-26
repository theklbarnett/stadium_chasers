from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.http import JsonResponse
import bcrypt

def render_home(request):
	if request.session.get('logged_on', False):
		return redirect('/dashboard')
	else:
		return render(request, 'home.html')

def render_signin(request):
	if request.session.get('logged_on', False):
		return redirect('/dashboard')
	else:
		return render(request, 'signin.html')

def render_register(request):
	if request.session.get('logged_on', False):
		return redirect('/dashboard')
	else:
		return render(request, 'register.html')

def render_user_dashboard(request):
	if request.session.get('logged_on', False):
		context = {
			'users': User.objects.all()
		}
		return render(request, 'dashboard.html', context)
	else:
		return redirect('/')

def render_add_user(request):
	if request.session.get('logged_on', False) and request.session.get('user_level', False) == 9:
		return render(request, 'add_user.html')
	else:
		return redirect('/')

def render_edit_profile(request):
	if request.session.get('logged_on', False):
		context = {
			'user': User.objects.get(id=request.session['user_id'])
		}
		return render(request, 'edit_user.html', context)
	else:
		return redirect('/')

def render_edit_user(request, id):
	if request.session.get('logged_on', False) and request.session.get('user_level', False) == 9:
		context = {
			'user': User.objects.get(id=id)
		}
		return render(request, 'edit_user.html', context)
	else:
		return redirect('/')


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

def email_uniqueness(request):
	email = request.GET.get('email', None)
	data = {
		'is_taken': User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

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

def logout(request):
	request.session.flush()
	return redirect('/')

def update_description(request):
	if request.method == "POST":
		c = User.objects.get(id=request.POST['id'])
		c.description = request.POST['description']
		c.save()
		messages.success(request, "Description successfully updated", extra_tags="description")
	return redirect(request.META.get('HTTP_REFERER'))

def update_info(request):
	if request.method == "POST":
		errors = User.objects.information_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value, extra_tags="info")
			return redirect(request.META.get('HTTP_REFERER'))
		else:
			c = User.objects.get(id=request.POST['id'])
			c.first_name = request.POST['first_name']
			c.last_name = request.POST['last_name']
			c.email = request.POST['email']
			if request.POST.get('user_level', False):
				c.user_level = request.POST['user_level']
			c.save()
			messages.success(request, "Information successfully updated", extra_tags="info")
			return redirect(request.META.get('HTTP_REFERER'))

def update_password(request):
	if request.method == "POST":
		errors = User.objects.password_change_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value, extra_tags="password")
			return redirect(request.META.get('HTTP_REFERER'))
		else:
			c = User.objects.get(id=request.POST['id'])
			c.password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
			c.save()
			messages.success(request, "Password successfully updated", extra_tags="password")
			return redirect(request.META.get('HTTP_REFERER'))

def remove_user(request, id):
	if request.session.get('logged_on', False) and request.session.get('user_level', False) == 9:
		User.objects.get(id=id).delete()
	return redirect('/dashboard')
