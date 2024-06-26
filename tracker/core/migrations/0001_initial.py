# Generated by Django 5.0.6 on 2024-06-12 22:01

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
            name='CoreUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CoreUserData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
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
    ]
