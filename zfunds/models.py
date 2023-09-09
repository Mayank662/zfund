from django.db import models
import uuid

# Create your models here.
USERTYPE = (
    ('ADMIN', 'Admin'),
    ('CLIENT', 'Client'),
    ('ADVISOR', 'Advisor'),
)

class ZUser(models.Model):
    account_type = models.CharField(max_length=10, choices=USERTYPE)  # null and blank is false
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=10, unique=True)
    is_self_registered = models.BooleanField(default=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user_created_by = models.IntegerField(null=True)


class Category(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(null=False, unique=True, max_length=20)


class Product(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    advisor_id = models.IntegerField()
    client_id = models.IntegerField()