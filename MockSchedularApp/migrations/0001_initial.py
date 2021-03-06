# Generated by Django 3.0.5 on 2020-08-25 10:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MockSchedular',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240, verbose_name='Name')),
                ('email', models.EmailField(max_length=254)),
                ('day', models.DateField(default=datetime.date.today)),
                ('time', models.TimeField()),
                ('about', models.CharField(default='DSA', max_length=20)),
            ],
        ),
    ]
