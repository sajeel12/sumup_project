# Generated by Django 4.2.7 on 2023-12-19 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_donor'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sumup_refresh_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
