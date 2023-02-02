from django.db import models

class AllManagers(models.Model):
    idManager = models.IntegerField(unique=True)
    name = models.CharField(max_length=95)

class SourceDeal(models.Model):
    idFromBitrix = models.IntegerField()
    title = models.CharField(max_length=95)

class SourceLead(models.Model):
    idFromBitrix = models.IntegerField()
    title = models.CharField(max_length=95)