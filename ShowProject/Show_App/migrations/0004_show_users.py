# Generated by Django 5.1 on 2024-10-07 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Show_App', '0003_alter_show_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='users',
            field=models.ManyToManyField(related_name='shows', to='Show_App.user'),
        ),
    ]
