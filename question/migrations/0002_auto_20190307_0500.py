# Generated by Django 2.1.7 on 2019-03-07 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='date',
            new_name='date_created',
        ),
    ]