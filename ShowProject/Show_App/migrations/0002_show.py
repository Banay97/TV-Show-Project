# Generated by Django 5.1 on 2024-10-07 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Show_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('network', models.CharField(max_length=50)),
                ('comment', models.TextField()),
                ('release_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
