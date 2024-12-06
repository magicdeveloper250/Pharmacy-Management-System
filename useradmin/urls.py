from django.urls import path
from .views import  dashboard, medicine

urlpatterns = [
    path("", dashboard.index, name="admin_dash"),
    path("medicine/", medicine.index, name="medicine"),
    path("upload_medicine/", medicine.upload_medicine, name="upload_medicine"),
    path('get_medicines/', medicine.get_medicines, name='get_medicines'),
    path('get_medicine/', medicine.get_medicine, name='get_medicine'),

]
