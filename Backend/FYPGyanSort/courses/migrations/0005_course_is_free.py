# Generated by Django 5.1.7 on 2025-04-19 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_content_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_free',
            field=models.BooleanField(default=False),
        ),
    ]
