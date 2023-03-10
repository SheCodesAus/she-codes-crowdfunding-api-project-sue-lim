# Generated by Django 4.1.5 on 2023-02-26 12:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0042_alter_project_liked_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='pledge',
            name='date_pledged',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
