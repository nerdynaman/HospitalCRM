# Generated by Django 5.0.4 on 2024-04-15 07:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0007_alter_session_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='result',
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('labTechnician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.labtechnician')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.session')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.test')),
            ],
        ),
    ]
