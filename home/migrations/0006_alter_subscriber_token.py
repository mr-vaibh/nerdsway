# Generated by Django 4.0.2 on 2022-02-22 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_subscriber_token_alter_subscriber_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='token',
            field=models.CharField(default='ikQw1KbaONO2XhmH', max_length=50),
        ),
    ]
