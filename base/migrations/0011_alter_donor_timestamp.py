# Generated by Django 5.0 on 2024-01-06 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_donor_amount_in_pounds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='timestamp',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]