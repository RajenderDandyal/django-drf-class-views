from statistics import mode
from django.db import models

# Create your models here.


class Profession(models.Model):
    description = models.CharField(max_length=50)


class DataSheet(models.Model):
    description = models.CharField(max_length=50)
    historical_data = models.TextField()


class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    professions = models.ManyToManyField(Profession)
    data_sheet = models.OneToOneField(DataSheet, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Document(models.Model):
    DOC_TYPES = (
        ('PP', "Passport"),
        ('ID', 'Identity card'),
        ('OT', 'Others'),
    )
    dtype = models.CharField(choices=DOC_TYPES, max_length=2)
    doc_number = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.doc_number
