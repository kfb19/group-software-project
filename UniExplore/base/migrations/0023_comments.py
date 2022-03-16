# Generated by Django 4.0.1 on 2022-03-14 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_alter_responses_photograph'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.responses')),
            ],
        ),
    ]
