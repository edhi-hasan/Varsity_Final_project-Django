# Generated by Django 5.0 on 2024-10-04 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodology', '0014_rename_blood_gorup_userprofile_blood_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='otp_expiration',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]