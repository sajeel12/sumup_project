# Generated by Django 4.2.7 on 2023-12-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sumup_access_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
