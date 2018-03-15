# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-09 20:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import picklefield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('popular_proposal', '0032_auto_20180308_1857'),
        ('elections', '0031_election_second_round'),
        ('backend_candidate', '0014_remove_suggesting_models')
    ]
    state_operations = [
        migrations.CreateModel(
            name='CandidateIncremental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.UUIDField(default=uuid.uuid4)),
                ('used', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.Candidate')),
            ],
        ),
        migrations.CreateModel(
            name='IncrementalsCandidateFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=12288, null=True)),
                ('subject', models.CharField(blank=True, max_length=256, null=True)),
                ('text', models.TextField(blank=True)),
                ('filter_qs', picklefield.fields.PickledObjectField(editable=False)),
                ('exclude_qs', picklefield.fields.PickledObjectField(editable=False)),
            ],
            options={
                'verbose_name': 'Filtro de propuestas para candidatos',
                'verbose_name_plural': 'Filtros de propuestas para candidatos',
            },
        ),
        migrations.CreateModel(
            name='ProposalSuggestionForIncremental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField(blank=True, default='')),
                ('sent', models.BooleanField(default=False)),
                ('incremental', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggestions', to='suggestions_for_candidates.IncrementalsCandidateFilter')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_proposals', to='popular_proposal.PopularProposal')),
            ],
        ),
        migrations.AddField(
            model_name='incrementalscandidatefilter',
            name='suggested_proposals',
            field=models.ManyToManyField(through='suggestions_for_candidates.ProposalSuggestionForIncremental', to='popular_proposal.PopularProposal'),
        ),
        migrations.AddField(
            model_name='candidateincremental',
            name='suggestion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='suggestions_for_candidates.IncrementalsCandidateFilter'),
        ),
    ]
    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]