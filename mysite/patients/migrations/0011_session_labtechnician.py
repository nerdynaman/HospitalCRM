# Generated by Django 5.0.4 on 2024-04-15 08:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0010_remove_session_testresults'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='labTechnician',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patients.labtechnician'),
        ),
    ]