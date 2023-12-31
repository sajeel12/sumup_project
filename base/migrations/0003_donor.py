# Generated by Django 5.0 on 2023-12-17 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_user_sumup_access_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('firstName', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=10)),
                ('phoneNumber', models.CharField(max_length=15)),
                ('emailAddress', models.EmailField(max_length=254)),
                ('transactionCode', models.CharField(blank=True, max_length=255, null=True)),
                ('amountInPounds', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('merchantCode', models.CharField(blank=True, max_length=255, null=True)),
                ('productInformation', models.TextField(blank=True, null=True)),
                ('subscribe', models.BooleanField(default=False)),
            ],
        ),
    ]
