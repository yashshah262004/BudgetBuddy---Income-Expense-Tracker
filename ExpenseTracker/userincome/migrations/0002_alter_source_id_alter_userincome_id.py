# Generated by Django 5.0.4 on 2024-10-11 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userincome', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userincome',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
