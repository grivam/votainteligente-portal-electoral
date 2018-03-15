# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-09 20:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend_candidate', '0013_auto_20171117_1432'),
    ]
    database_operations = [
        migrations.AlterModelTable('IncrementalsCandidateFilter', 'suggestions_for_candidates_incrementalscandidatefilter'),
        migrations.AlterModelTable('CandidateIncremental', 'suggestions_for_candidates_candidateincremental'),
        migrations.AlterModelTable('ProposalSuggestionForIncremental', 'suggestions_for_candidates_proposalsuggestionforincremental')
    ]

    state_operations = [
        migrations.DeleteModel('IncrementalsCandidateFilter'),
        migrations.DeleteModel('CandidateIncremental'),
        migrations.DeleteModel('ProposalSuggestionForIncremental')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
                database_operations=database_operations,
                state_operations=state_operations)
    ]