


from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modelvar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255)),
                ('created_by', models.IntegerField(null=True)),
                ('percent_value', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StripeCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripeCustomerId', models.CharField(max_length=300, null=True)),
                ('stripeSubscriptionId', models.CharField(max_length=255, null=True)),
                ('membershipstatus', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=200, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('title', models.CharField(max_length=200, null=True)),
                ('password', models.CharField(max_length=220)),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('zip', models.IntegerField(max_length=6, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('phone_number', phone_field.models.PhoneField(default=0, max_length=31, null=True)),
                ('terms_and_condition', models.BooleanField(default=0)),
                ('entry_code', models.CharField(max_length=200, null=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.\t\tUnselect this instead of deleting accounts.')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
