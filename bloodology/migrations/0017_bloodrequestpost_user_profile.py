# Generated by Django 5.0 on 2024-10-05 08:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodology', '0016_blogpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodrequestpost',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bloodology.userprofile'),
        ),
    ]