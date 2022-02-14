# Generated by Django 3.1.2 on 2022-02-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accept', 'Accept'), ('reject', 'Reject')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='visit',
            name='time',
            field=models.DateTimeField(),
        ),
    ]