# Generated by Django 3.2.25 on 2024-04-08 16:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_purchase_purchaseitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 8, 16, 18, 20, 897446, tzinfo=utc)),
        ),
    ]