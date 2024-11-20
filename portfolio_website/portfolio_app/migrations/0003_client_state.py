# Generated by Django 5.1.2 on 2024-10-29 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0002_service_alter_portfolio_service_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='state',
            field=models.CharField(choices=[(0, 'Active'), (1, 'Archived')], default='Active', max_length=10, verbose_name='State'),
        ),
    ]