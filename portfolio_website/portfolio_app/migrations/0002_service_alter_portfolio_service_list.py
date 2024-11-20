# Generated by Django 5.1.2 on 2024-10-21 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='Value')),
            ],
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='service_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio_app.service'),
        ),
    ]