# Generated by Django 3.1.7 on 2021-04-10 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20210410_0951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheduledtransaction',
            name='type',
        ),
    ]