# Generated by Django 4.0.1 on 2022-03-16 12:55

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_merge_20220315_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='profile_pictures/placeholder.png', upload_to=base.models.content_file_name),
        ),
        migrations.DeleteModel(
            name='WeeklyChallenge',
        ),
    ]
