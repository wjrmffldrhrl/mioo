# Generated by Django 2.2.4 on 2019-08-20 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('size', models.CharField(max_length=30)),
            ],
        ),
    ]
