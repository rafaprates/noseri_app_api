# Generated by Django 3.2.4 on 2021-08-07 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_userloadassociation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userloadassociation',
            name='load',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.load'),
        ),
    ]
