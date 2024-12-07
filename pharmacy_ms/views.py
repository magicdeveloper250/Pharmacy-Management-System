from django.shortcuts import render
from django.contrib.auth.decorators import login_not_required

@login_not_required
def index(request):
    return render(request, "index.html")
