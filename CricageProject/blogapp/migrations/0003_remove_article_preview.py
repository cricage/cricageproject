# Generated by Django 2.2 on 2020-08-12 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_auto_20200812_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='preview',
        ),
    ]
