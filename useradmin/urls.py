from django.urls import path
from .views import  dashboard, medicine, customer, supplier

urlpatterns = [
    path("", dashboard.index, name="admin_dash"),
    path("medicine/", medicine.index, name="medicine"),
    path("upload_medicine/", medicine.upload_medicine, name="upload_medicine"),
    path('update_medicine/', medicine.update_medicine, name='update_medicine'),
    path('delete_medicine/', medicine.delete_medicine, name='delete_medicine'),
    path('get_medicines/', medicine.get_medicines, name='get_medicines'),
    path('get_medicine/', medicine.get_medicine, name='get_medicine'),
    path("customer/", customer.index, name="customer"),
    path("add_customer/", customer.add_customer, name="add_customer"),
    path('update_customer/', customer.update_customer, name='update_customer'),
    path('delete_customer/', customer.delete_customer, name='delete_customer'),
    path('get_customers/', customer.get_customers, name='get_customers'),
    path('get_customer/', customer.get_customer, name='get_customer'),
    path("supplier/", supplier.index, name="supplier"),
    path("add_supplier/", supplier.add_supplier, name="add_supplier"),
    path('update_supplier/', supplier.update_supplier, name='update_supplier'),
    path('delete_supplier/', supplier.delete_supplier, name='delete_supplier'),
    path('get_suppliers/', supplier.get_suppliers, name='get_suppliers'),
    path('get_supplier/', supplier.get_supplier, name='get_supplier'),

]
