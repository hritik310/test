# Generated by Django 3.2.8 on 2021-11-23 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_temporary_permits_permit_hour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurance',
            name='policy_number',
            field=models.BigIntegerField(),
        ),
    ]