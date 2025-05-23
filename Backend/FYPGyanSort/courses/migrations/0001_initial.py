# Generated by Django 5.1.7 on 2025-04-01 10:47

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instructors', '0005_alter_instructor_verification_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('course_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('course_thumbnail', models.ImageField(upload_to='course_thumbnails/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('demo_video', models.FileField(upload_to='course_demos/', validators=[django.core.validators.FileExtensionValidator(['mp4', 'webm'])])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.category')),
                ('instructor', models.ForeignKey(limit_choices_to={'is_active': True, 'verification_status': 'verified'}, on_delete=django.db.models.deletion.CASCADE, to='instructors.instructor')),
                ('reviews', models.ManyToManyField(blank=True, to='courses.review')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
