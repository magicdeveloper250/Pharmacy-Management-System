from django.shortcuts import render


def index(request):
    tab = request.GET.get('tab', 'dash')  
    return render(request, 'dashboard.html', {'active_tab': tab})

