# Generated by Django 4.1.5 on 2023-01-26 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_remove_comment_content_comment_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='created_at',
        ),
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Comment'),
        ),
    ]
