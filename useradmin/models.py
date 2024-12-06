from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    formulation = models.CharField(max_length=255)
    strength = models.CharField(max_length=100)
    expiration_date = models.DateField()
    batch_number = models.CharField(max_length=100)
    storage_conditions = models.TextField()
    manufacturer = models.CharField(max_length=255)
    active_ingredients = models.TextField()
    shelf_life = models.PositiveIntegerField(help_text="Shelf life in months")
    route_of_administration = models.CharField(max_length=100)
    dosage_instructions = models.TextField()
    side_effects = models.TextField()
    packaging_type = models.CharField(max_length=100)
    quantity_in_stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_prescription_required = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name



class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    address = models.TextField()
    lead_time = models.PositiveIntegerField(help_text="Lead time in days")
    payment_terms = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name



class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    allergies = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class Prescription(models.Model):
    consumer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=255)
    prescription_date = models.DateField()
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    
    def __str__(self):
        return f"Prescription for {self.consumer} on {self.prescription_date}"



class Purchase(models.Model):
    consumer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Purchase by {self.consumer} on {self.purchase_date}"
    
    def save(self, *args, **kwargs):
        # Calculate total price when saving
        self.total_price = self.quantity * self.medicine.price
        super().save(*args, **kwargs)
