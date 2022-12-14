# Generated by Django 4.0.2 on 2022-05-13 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_modelname_modelname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Var',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Selectvar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('percent_value', models.IntegerField(null=True)),
                ('varid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.var')),
            ],
        ),
    ]
