# Generated by Django 5.0.7 on 2024-08-05 21:51

import core.models.core
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import phone_field.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', max_length=255, null=True)),
                ('responsible_party_email', models.EmailField(max_length=255)),
                ('responsible_party_phone', phone_field.models.PhoneField(max_length=31)),
                ('address_line_1', models.CharField(max_length=255)),
                ('address_line_2', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('postal_code', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('timezone', models.CharField(default='UTC', max_length=255)),
            ],
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CoreUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['core_user_data__last_name', 'core_user_data__email'],
            },
            bases=(models.Model, core.models.core.CoreModelActiveManager, core.models.core.CoreModelManager),
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CoreUserData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name_prefix', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('name_suffix', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=255)),
                ('secondary_email', models.EmailField(blank=True, max_length=255, null=True)),
                ('home_phone', phone_field.models.PhoneField(blank=True, max_length=31, null=True)),
                ('mobile_phone', phone_field.models.PhoneField(blank=True, max_length=31, null=True)),
                ('work_phone', phone_field.models.PhoneField(blank=True, max_length=31, null=True)),
                ('address_line_1', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('address_line_2', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('city', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('state', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('timezone', models.CharField(default='UTC', max_length=255)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='coreuser',
            name='core_user_data',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.coreuserdata'),
        ),
        migrations.CreateModel(
            name='DeletedModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('hard_deleted', models.BooleanField(default=False)),
                ('soft_deleted', models.BooleanField(default=False)),
                ('deleted_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
            ],
        ),
        migrations.AddField(
            model_name='coreuserdata',
            name='deleted',
            field=models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel'),
        ),
        migrations.AddField(
            model_name='coreuser',
            name='deleted',
            field=models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel'),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('renewal_date', models.DateField(blank=True, null=True)),
                ('number_users_allowed', models.IntegerField(default=5)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('members', models.ManyToManyField(related_name='organizationmembers_set', to='core.coreuser')),
            ],
            options={
                'ordering': ['organization_data__name'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
