# Generated by Django 2.1.7 on 2019-02-28 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='informarion',
            new_name='information',
        ),
    ]