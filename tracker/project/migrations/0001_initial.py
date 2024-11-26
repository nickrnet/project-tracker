# Generated by Django 5.1.1 on 2024-10-24 14:50

import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuiltInIssuePriority',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('name', 'description')},
            },
        ),
        migrations.CreateModel(
            name='BuiltInIssueSeverity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
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
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
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
                ('archived', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('BUG', 'Bug'), ('DOCUMENTATION', 'Documentation'), ('ENHANCEMENT', 'Enhancement'), ('EPIC', 'Epic'), ('FEATURE', 'Feature'), ('IMPROVEMENT', 'Improvement'), ('PROPOSAL', 'Proposal'), ('QUESTION', 'Question'), ('SPIKE', 'Spike'), ('STORY', 'Story'), ('SUB_TASK', 'Sub-task'), ('TASK', 'Task'), ('TEST', 'Test')], max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['type'],
                'unique_together': {('type', 'description')},
            },
        ),
        migrations.CreateModel(
            name='ComponentData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('label', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('current', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.componentdata')),
            ],
            options={
                'ordering': ['current__name'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomIssuePriorityData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['name'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomIssuePriority',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('current', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.customissueprioritydata')),
            ],
            options={
                'ordering': ['current__name'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomIssueSeverityData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['name'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomIssueSeverity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('current', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.customissueseveritydata')),
            ],
            options={
                'ordering': ['current__name'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomIssueStatusData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['name'],
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
                ('archived', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('current', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.customissuestatusdata')),
            ],
            options={
                'ordering': ['current__name'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomIssueTypeData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['name'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomIssueType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('current', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.customissuetypedata')),
            ],
            options={
                'ordering': ['current__name'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='GitRepositoryData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('url', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'abstract': False,
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
                ('archived', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('current', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.gitrepositorydata')),
            ],
            options={
                'ordering': ['current__name', 'current__url'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='IssueData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('summary', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issueassignee_set', to='core.coreuser')),
                ('built_in_priority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.builtinissuepriority')),
                ('built_in_severity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.builtinissueseverity')),
                ('built_in_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.builtinissuestatus')),
                ('built_in_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.builtinissuetype')),
                ('component', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.component')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('custom_priority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.customissuepriority')),
                ('custom_severity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.customissueseverity')),
                ('custom_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.customissuestatus')),
                ('custom_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.customissuetype')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issuereporter_set', to='core.coreuser')),
                ('watchers', models.ManyToManyField(related_name='issuewatcher_set', to='core.coreuser')),
            ],
            options={
                'abstract': False,
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
                ('archived', models.BooleanField(default=False)),
                ('sequence', models.PositiveIntegerField()),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('current', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.issuedata')),
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
                ('archived', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'ordering': ['current__name'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='issuedata',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
        migrations.AddField(
            model_name='component',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
        migrations.CreateModel(
            name='ProjectData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_private', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('git_repositories', models.ManyToManyField(to='project.gitrepository')),
                ('users', models.ManyToManyField(to='core.coreuser')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='current',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.projectdata'),
        ),
        migrations.CreateModel(
            name='ProjectLabel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='projectdata',
            name='label',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='project.projectlabel'),
        ),
        migrations.CreateModel(
            name='ProjectLabelData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('color', models.CharField(default='#000000', max_length=7)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='projectlabel',
            name='current',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.projectlabeldata'),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
            ],
            options={
                'ordering': ['current__name'],
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='issuedata',
            name='version',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.version'),
        ),
        migrations.CreateModel(
            name='VersionData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('archived', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('release_date', models.DateField(blank=True, default='', null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to='core.coreuser')),
                ('deleted', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.deletedmodel')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='version',
            name='current',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='project.versiondata'),
        ),
    ]
