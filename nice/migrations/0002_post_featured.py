# Generated by Django 2.2.6 on 2019-10-17 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='featured',
            field=models.BooleanField(default='False'),
            preserve_default=False,
        ),
    ]
