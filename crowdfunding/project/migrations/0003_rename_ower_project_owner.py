# Generated by Django 5.1 on 2024-10-08 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_pledge_supporter_project_ower'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='ower',
            new_name='owner',
        ),
    ]
