# Generated by Django 3.2.4 on 2021-07-24 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_tax'),
    ]

    operations = [
        migrations.CreateModel(
            name='KwhTotal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kwh_sum', models.FloatField()),
                ('data', models.CharField(max_length=32)),
            ],
        ),
    ]