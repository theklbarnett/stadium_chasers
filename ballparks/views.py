from django.shortcuts import render, redirect

def login_page(request):
	return render(request, 'login.html')

def login_user(request):
	return redirect('/home')

def create_user(request):
	return redirect('/home')

def homepage(request):
	return render(request, 'homepage.html')

def render_park(request):
	pass
