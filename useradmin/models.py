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
    def to_json(self):
        return {'id': self.id,
                'name': self.name,
                'formulation': self.formulation,
                'strength': self.strength,
                'expiration_date': self.expiration_date,
                'batch_number': self.batch_number,
                'storage_conditions': self.storage_conditions,
                'manufacturer': self.manufacturer,
                'active_ingredients': self.active_ingredients,
                'shelf_life': self.shelf_life,
                'route_of_administration': self.route_of_administration,
                'dosage_instructions': self.dosage_instructions,
                'side_effects': self.side_effects,
                'packaging_type': self.packaging_type,
                'quantity_in_stock': self.quantity_in_stock,
                'price': self.price,
                'is_prescription_required': self.is_prescription_required,}


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
    def to_json(self):
        return  {
                'id': self.id,
                'name': self.name,
                'contact_name': self.contact_name,
                'contact_phone': self.contact_phone,
                'contact_email': self.contact_email,
                'address': self.address,
                'lead_time':self.lead_time,
                'payment_terms':self.payment_terms
            }



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
    def to_json(self):
        return   {
                'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'phone_number': self.phone_number,
                "date_of_birth":self.date_of_birth,
                "address":self.address,
                "allergies":self.allergies
            }





class Prescription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=255)
    prescription_date = models.DateField()
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    
    def __str__(self):
        return f"Prescription for {self.consumer} on {self.prescription_date}"



class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Purchase by {self.consumer} on {self.purchase_date}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.medicine.price
        super().save(*args, **kwargs)


class Sales(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    sale_date =  models.DateField(auto_now_add=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('ONLINE', 'Online Payment'),
    ], default='CASH')

    def __str__(self):
        return f"Sale to {self.customer} on {self.sale_date}"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.medicine.price
        if self.medicine.quantity_in_stock < self.quantity:
            raise ValueError("Not enough stock for the requested sale.")
        super().save(*args, **kwargs)

    def to_json(self):
        return {
            'id': self.id,
            'customer': self.customer.to_json(),
            'medicine': self.medicine.to_json(),
            'quantity': self.quantity,
            'total_price': self.total_price,
            'sale_date': self.sale_date,
            'prescription': self.prescription.id if self.prescription else None,
            'payment_method': self.payment_method,
        }