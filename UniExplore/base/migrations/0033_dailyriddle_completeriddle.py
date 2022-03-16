# Generated by Django 4.0.1 on 2022-03-16 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0032_alter_responses_photograph'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyRiddle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('points', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lat', models.FloatField(default=0)),
                ('long', models.FloatField(default=0)),
                ('answer', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompleteRiddle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('riddle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complete_riddle', to='base.dailyriddle')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]