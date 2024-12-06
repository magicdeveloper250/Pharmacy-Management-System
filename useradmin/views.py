from django.shortcuts import render, redirect


def admin_index(request):
    return render(request, "admin_dashboard.html")

