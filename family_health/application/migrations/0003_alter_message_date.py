# Generated by Django 4.2.5 on 2024-01-03 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_message_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
