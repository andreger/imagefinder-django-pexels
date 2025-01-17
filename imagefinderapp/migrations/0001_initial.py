# Generated by Django 5.0.6 on 2024-05-30 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PexelsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=2048)),
                ('previewURL', models.URLField(max_length=2048)),
                ('photographer', models.CharField(max_length=255)),
            ],
        ),
    ]
