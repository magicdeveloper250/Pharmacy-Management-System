# Generated by Django 5.1.4 on 2024-12-09 05:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("useradmin", "0002_rename_consumer_purchase_supplier"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchase",
            name="supplier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="useradmin.supplier"
            ),
        ),
    ]
