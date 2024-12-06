# Generated by Django 5.1.4 on 2024-12-06 15:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("date_of_birth", models.DateField()),
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.CharField(max_length=15)),
                ("address", models.TextField()),
                ("allergies", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Medicine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("formulation", models.CharField(max_length=255)),
                ("strength", models.CharField(max_length=100)),
                ("expiration_date", models.DateField()),
                ("batch_number", models.CharField(max_length=100)),
                ("storage_conditions", models.TextField()),
                ("manufacturer", models.CharField(max_length=255)),
                ("active_ingredients", models.TextField()),
                (
                    "shelf_life",
                    models.PositiveIntegerField(help_text="Shelf life in months"),
                ),
                ("route_of_administration", models.CharField(max_length=100)),
                ("dosage_instructions", models.TextField()),
                ("side_effects", models.TextField()),
                ("packaging_type", models.CharField(max_length=100)),
                ("quantity_in_stock", models.PositiveIntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("is_prescription_required", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Supplier",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("contact_name", models.CharField(max_length=255)),
                ("contact_email", models.EmailField(max_length=254)),
                ("contact_phone", models.CharField(max_length=15)),
                ("address", models.TextField()),
                (
                    "lead_time",
                    models.PositiveIntegerField(help_text="Lead time in days"),
                ),
                ("payment_terms", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Prescription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("doctor_name", models.CharField(max_length=255)),
                ("prescription_date", models.DateField()),
                ("dosage", models.CharField(max_length=100)),
                ("instructions", models.TextField()),
                (
                    "consumer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="useradmin.customer",
                    ),
                ),
                (
                    "medicine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="useradmin.medicine",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Purchase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("purchase_date", models.DateField(auto_now_add=True)),
                (
                    "consumer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="useradmin.customer",
                    ),
                ),
                (
                    "medicine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="useradmin.medicine",
                    ),
                ),
            ],
        ),
    ]
