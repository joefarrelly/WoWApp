# Generated by Django 3.0.6 on 2020-06-17 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BoostApp', '0002_auto_20200616_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertiser',
            name='advCommission',
            field=models.DecimalField(decimal_places=2, max_digits=2),
        ),
    ]
