# Generated by Django 3.2.6 on 2022-03-21 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rank',
            name='last_use',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
