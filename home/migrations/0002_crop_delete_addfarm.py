# Generated by Django 5.1.5 on 2025-03-10 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop_name', models.CharField(max_length=100)),
                ('farm_name', models.CharField(max_length=100)),
                ('crop_description', models.TextField()),
                ('crop_budget', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='AddFarm',
        ),
    ]
