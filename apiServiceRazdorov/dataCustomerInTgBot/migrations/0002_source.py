# Generated by Django 4.1.5 on 2023-01-21 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataCustomerInTgBot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idFromBitrix', models.IntegerField()),
                ('title', models.CharField(max_length=95)),
            ],
        ),
    ]