# Generated by Django 5.0.1 on 2024-03-06 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_alter_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.TextField(blank=True, null=True),
        ),
    ]