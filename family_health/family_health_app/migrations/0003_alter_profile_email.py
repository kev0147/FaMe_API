# Generated by Django 4.2.5 on 2023-11-04 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family_health_app', '0002_remove_patient_balance_delete_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]