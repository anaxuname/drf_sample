# Generated by Django 5.0.2 on 2024-02-13 21:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Course name')),
                ('preview_course', models.ImageField(blank=True, null=True, upload_to='course', verbose_name='Course image')),
                ('description', models.TextField(verbose_name='Course description')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Lesson name')),
                ('preview_lesson', models.ImageField(blank=True, null=True, upload_to='course', verbose_name='Lesson image')),
                ('description', models.TextField(verbose_name='Lesson description')),
                ('link', models.CharField(max_length=200, verbose_name='Lesson link')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.course', verbose_name='Course pk')),
            ],
            options={
                'verbose_name': 'Lesson',
                'verbose_name_plural': 'Lessons',
            },
        ),
    ]
