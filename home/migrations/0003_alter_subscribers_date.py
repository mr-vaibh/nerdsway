# Generated by Django 4.0.2 on 2022-02-21 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribers',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
