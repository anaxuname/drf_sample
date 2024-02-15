# Generated by Django 5.0.2 on 2024-02-13 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='users', verbose_name='Avater'),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(default='Moscow', max_length=50, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(default='s', max_length=255, verbose_name='Full Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='1', max_length=50, verbose_name='Phone_number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
    ]
