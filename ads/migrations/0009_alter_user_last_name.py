# Generated by Django 4.0.1 on 2023-02-12 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0008_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
