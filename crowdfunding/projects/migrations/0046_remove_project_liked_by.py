# Generated by Django 4.1.5 on 2023-07-25 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0045_project_liked_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='liked_by',
        ),
    ]
