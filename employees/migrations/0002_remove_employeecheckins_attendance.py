# Generated by Django 3.1.7 on 2021-07-07 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeecheckins',
            name='attendance',
        ),
    ]
