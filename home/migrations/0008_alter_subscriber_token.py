# Generated by Django 4.0.2 on 2022-02-23 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_subscriber_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='token',
            field=models.CharField(default='5LY8OvfblDc0GEVL', max_length=50),
        ),
    ]