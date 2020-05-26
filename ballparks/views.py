from django.shortcuts import render

def login_user(request):
	return render(request, 'login.html')

def homepage(request):
	return render(request, 'homepage.html')

def render_park(request):
	pass
