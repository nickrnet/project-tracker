# Generated by Django 5.0.6 on 2024-07-03 03:25

import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuiltInIssuePriority',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('name', 'description')},
            },
        ),
        migrations.CreateModel(
            name='BuiltInIssueStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('name', 'description')},
            },
        ),
        migrations.CreateModel(
            name='BuiltInIssueType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('type', models.CharField(choices=[('BUG', 'Bug'), ('DOCUMENTATION', 'Documentation'), ('ENHANCEMENT', 'Enhancement'), ('EPIC', 'Epic'), ('FEATURE', 'Feature'), ('IMPROVEMENT', 'Improvement'), ('PROPOSAL', 'Proposal'), ('QUESTION', 'Question'), ('SPIKE', 'Spike'), ('STORY', 'Story'), ('SUB_TASK', 'Sub-task'), ('TASK', 'Task'), ('TEST', 'Test')], max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['type'],
                'unique_together': {('type', 'description')},
            },
        ),
        migrations.CreateModel(
            name='CustomIssueType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('name', 'description')},
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='GitRepository',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['name', 'url'],
                'unique_together': {('name', 'url')},
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('summary', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issueassignee_set', to=settings.AUTH_USER_MODEL)),
                ('built_in_priority', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.builtinissuepriority')),
                ('built_in_status', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.builtinissuestatus')),
                ('built_in_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.builtinissuetype')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
                ('custom_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.customissuetype')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issuereporter_set', to=settings.AUTH_USER_MODEL)),
                ('watchers', models.ManyToManyField(related_name='issuewatchers_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('label', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_private', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('git_repository', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.gitrepository')),
                ('issues', models.ManyToManyField(related_name='projectissues_set', to='project.issue')),
                ('users', models.ManyToManyField(related_name='projectusers_set', to='core.coreuser')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('name', 'git_repository')},
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectissues_set', to='project.project'),
        ),
        migrations.CreateModel(
            name='CustomIssuePriority',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('name', 'description')},
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomIssueStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('name', 'description')},
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
