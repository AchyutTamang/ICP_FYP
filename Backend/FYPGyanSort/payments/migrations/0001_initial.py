# Generated by Django 5.1.7 on 2025-04-19 06:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('payment_type', models.CharField(choices=[('khalti', 'Khalti'), ('cash', 'Cash')], default='khalti', max_length=20)),
                ('user_email', models.EmailField(max_length=254)),
                ('user_type', models.CharField(choices=[('student', 'Student'), ('instructor', 'Instructor')], max_length=20)),
                ('user_id', models.IntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_name', models.CharField(default='GyanSort Course', max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('pidx', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
