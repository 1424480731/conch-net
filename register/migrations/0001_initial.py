# Generated by Django 2.2.11 on 2020-03-15 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('birthday', models.CharField(max_length=50)),
                ('id_card_num', models.CharField(max_length=50)),
                ('habby', models.TextField(max_length=500)),
                ('real_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
    ]
