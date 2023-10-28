# Generated by Django 4.2.6 on 2023-10-28 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_camera_camera_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='camera_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='camera',
            name='camera_name',
            field=models.CharField(max_length=500, null=True, unique=True),
        ),
    ]
