# Generated by Django 4.2.5 on 2023-09-08 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zfunds', '0002_remove_zuser_admin_id_remove_zuser_advisor_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='zuser',
            name='user_created_by',
            field=models.IntegerField(null=True),
        ),
    ]