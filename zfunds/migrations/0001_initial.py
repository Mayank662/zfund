# Generated by Django 4.2.5 on 2023-09-08 12:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('cid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('purchase_id', models.IntegerField(primary_key=True, serialize=False)),
                ('product_id', models.IntegerField()),
                ('advisor_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ZUser',
            fields=[
                ('account_type', models.CharField(choices=[('ADMIN', 'Admin'), ('USER', 'Customer'), ('ADVISOR', 'Advisor')], max_length=10)),
                ('admin_id', models.IntegerField(null=True, unique=True)),
                ('user_id', models.IntegerField(null=True, unique=True)),
                ('advisor_id', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=30, null=True)),
                ('phone', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('is_self_registered', models.BooleanField(default=True)),
                ('key', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zfunds.category')),
            ],
        ),
    ]