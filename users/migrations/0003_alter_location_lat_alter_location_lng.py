# Generated by Django 4.0.1 on 2023-02-12 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_location_is_active_alter_location_lat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='lng',
            field=models.FloatField(null=True),
        ),
    ]
