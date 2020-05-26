from django.shortcuts import render

def render_login(request):
	return render(request, 'login.html')

def render_home(request):
	return render(request, 'homepage.html')

def render_park(request):
	pass
