# Generated by Django 4.0.2 on 2022-02-10 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_name_user_first_name_remove_user_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
