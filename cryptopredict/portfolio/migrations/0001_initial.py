# Generated by Django 5.1.1 on 2024-10-05 19:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_created', models.DateField()),
                ('time_created', models.TimeField()),
                ('cryptoName', models.CharField(max_length=30)),
                ('cryptoQuantity', models.FloatField()),
                ('price', models.FloatField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['cryptoName', 'time_created', 'day_created'],
            },
        ),
        migrations.CreateModel(
            name='CryptoWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cryptoName', models.CharField(max_length=30)),
                ('cryptoQuantity', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['cryptoName'],
            },
        ),
        migrations.CreateModel(
            name='DepositWithdraw_Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_created', models.DateField()),
                ('time_created', models.TimeField()),
                ('type', models.CharField(max_length=15)),
                ('quantity', models.FloatField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-day_created', '-time_created'],
            },
        ),
    ]
