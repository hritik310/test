# Generated by Django 3.2.9 on 2021-11-23 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_insurance_policy_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurance',
            name='insurer',
            field=models.CharField(default='', max_length=255),
        ),
    ]
