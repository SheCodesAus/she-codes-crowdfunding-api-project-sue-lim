# Generated by Django 4.1.5 on 2023-01-20 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_project_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='date_created',
            field=models.DateTimeField(verbose_name='d-m-Y'),
        ),
    ]
