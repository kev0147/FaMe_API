# Generated by Django 4.2.5 on 2023-11-02 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_health_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='balance',
        ),
        migrations.DeleteModel(
            name='Balance',
        ),
    ]
