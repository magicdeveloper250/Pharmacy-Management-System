# Generated by Django 5.1.4 on 2024-12-09 05:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("useradmin", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="purchase",
            old_name="consumer",
            new_name="supplier",
        ),
    ]
