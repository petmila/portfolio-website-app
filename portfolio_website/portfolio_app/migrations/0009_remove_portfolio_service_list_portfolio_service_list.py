# Generated by Django 5.1.3 on 2024-11-23 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0008_alter_client_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='service_list',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='service_list',
            field=models.ManyToManyField(blank=True, to='portfolio_app.service'),
        ),
    ]
