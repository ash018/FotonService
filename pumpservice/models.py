from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.auth.models import AbstractUser
from smart_selects.db_fields import ChainedForeignKey

class Territory(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TerritoryID')
    Name = models.CharField(max_length=100, db_column='TerritoryName')
    Code = models.CharField(max_length=50, db_column='TerritoryCode')

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name='Territory'
        managed = True
        db_table = 'Territory'

class AppUser(models.Model):
    Id = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=50, db_column='UserName')
    Password = models.CharField(max_length=50, db_column='Password')
    TerritoryId = models.ForeignKey(Territory, db_column='TerritoryId', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.UserName

    class Meta:
        managed = True
        db_table = 'AppUser'

class ServiceDetails(models.Model):
    Id = models.AutoField(primary_key=True, db_column='ServiceDetailsId')
    CustomerName = models.CharField(max_length=100, db_column='CustomerName', default='N/A')
    CustomerCode = models.CharField(max_length=100, db_column='CustomerCode', default='N/A')
    Mobile = models.CharField(max_length=20,db_column='Mobile', default='N/A')
    ServicePortFolio = models.CharField(max_length=100,db_column='ServicePortFolio', default='N/A')
    ServiceCount = models.CharField(max_length=100, db_column='ServiceCount', default='N/A')#KEY_SERVICETIME
    ProductModel = models.CharField(max_length=100, db_column='ProductModel', default='N/A')#KEY_MODEL

    ServiceDemandDate = models.DateTimeField(db_column='ServiceDemandDate')#KEY_COMPLAINDATE
    ServiceStartDate = models.DateTimeField(db_column='ServiceStartDate')#KEY_ATTENDATE
    #ServiceEndDate = models.DateTimeField(db_column='ServiceEndDate')
    ServiceIncome = models.FloatField(db_column='ServiceIncome', default=0.0)# KEY_SERVICECHARGE
    VisitDate = models.DateTimeField(db_column='VisitDate')#KEY_ATTENDATE

    #MobileCreatedDT = models.DateTimeField(db_column='MobileCreatedDT', auto_now_add=True)
    #MobileEditedDT = models.DateTimeField(db_column='MobileEditedDT', auto_now_add=True)
    #MobileLogCount = models.IntegerField(db_column='MobileLogCount',default=0)
    Latitude = models.DecimalField(max_digits=18, decimal_places=8, db_column='Latitude', default=0.0)#KEY_SLAT
    Longitude = models.DecimalField(max_digits=18, decimal_places=8, db_column='Longitude', default=0.0)#KEY_SLANG
    MobileId = models.IntegerField(db_column='MobileId', default=0)
    ServerInsertDateTime = models.DateTimeField(auto_now_add=True)
    ServerUpdateDateTime = models.DateTimeField(auto_now=True)

    #ServiceRatting = models.CharField(db_column='ServiceRatting', max_length=20, default='0')
    UserId = models.ForeignKey(AppUser, db_column='AppUserId', on_delete=models.CASCADE)

    def __str__(self):
        return self.CustomerName

    class Meta:
        verbose_name_plural = 'Service Details'
        managed = True
        db_table = 'ServiceDetails'

