# Generated by Django 4.0.2 on 2022-02-22 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_rename_subscribers_subscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='token',
            field=models.CharField(default='4hpc4p2rSVRERHBN', max_length=50),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.EmailField(default='', max_length=100),
        ),
    ]