# Generated by Django 3.1.7 on 2021-04-10 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_remove_scheduledtransaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(blank=True, default='', max_length=1),
        ),
    ]
