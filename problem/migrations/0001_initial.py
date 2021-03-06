# Generated by Django 2.0.4 on 2018-04-20 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('picture', models.FileField(blank=True, upload_to='')),
                ('input', models.TextField(blank=True)),
                ('output', models.TextField(blank=True)),
                ('sample_input', models.TextField(blank=True)),
                ('sample_output', models.TextField(blank=True)),
                ('hint', models.TextField(blank=True)),
            ],
        ),
    ]
