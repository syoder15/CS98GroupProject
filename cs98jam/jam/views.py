from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    context = {}
    return render(request, 'jam/index.html', context)
