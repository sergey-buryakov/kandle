# Generated by Django 2.0.5 on 2018-05-29 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kandleapp', '0003_auto_20180529_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='startTime',
            field=models.TimeField(null=True),
        ),
    ]