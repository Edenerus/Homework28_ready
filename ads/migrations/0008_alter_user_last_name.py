# Generated by Django 4.0.1 on 2023-02-12 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0007_alter_ad_description_alter_ad_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
