from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {}
    return render(request, 'jam/index.html', context)

def profile(request):
	context = {}
	return render(request, 'jam/profile.html', context)
