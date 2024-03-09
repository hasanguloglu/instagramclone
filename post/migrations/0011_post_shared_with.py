# Generated by Django 5.0.1 on 2024-03-07 22:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_alter_comment_post'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='shared_with',
            field=models.ManyToManyField(blank=True, null=True, related_name='shared_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
