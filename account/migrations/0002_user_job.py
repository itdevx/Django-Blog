# Generated by Django 4.1.4 on 2023-01-15 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='job',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]