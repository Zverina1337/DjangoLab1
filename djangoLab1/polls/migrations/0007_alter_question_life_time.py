# Generated by Django 4.1.3 on 2022-12-12 15:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_alter_question_life_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='life_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 13, 15, 27, 54, 597579), verbose_name='Время жизни'),
        ),
    ]
