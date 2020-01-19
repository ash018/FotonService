from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.auth.models import AbstractUser
from smart_selects.db_fields import ChainedForeignKey
# Create your models here.

class RowStatus(models.Model):
    Id = models.AutoField(primary_key=True, db_column='RowStatusId')
    Name = models.CharField(max_length=10, db_column='Name')

    def __str__(self):
        return self.Name

    class Meta:
        managed = False
        db_table = 'RowStatus'

class Territory(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TerritoryId')
    Name = models.CharField(max_length=100, db_column='TerritoryName')
    Code = models.CharField(max_length=50, db_column='TerritoryCode')
    Notes = models.CharField(max_length=100, db_column='Notes')

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name='Territory'
        managed = False
        db_table = 'Territory'

class Area(models.Model):
    Id = models.AutoField(primary_key=True, db_column='AreaId')
    AreaName = models.CharField(max_length=100, db_column='AreaName', unique=True)
    TerritoryId = models.ManyToManyField(Territory, db_column='TerritoryId', verbose_name='Territory')

    def __str__(self):
        return self.AreaName

    class Meta:
        managed = False
        db_table = 'Area'


class UserArea(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    UserId = models.ForeignKey(User,db_column='UserId',on_delete=models.CASCADE, verbose_name='Engineer')
    AreaId = models.ManyToManyField(Area, db_column='AreaId', verbose_name='Area')

    class Meta:
        verbose_name='Assign User Area'
        managed = False
        db_table = 'UserArea'

class MotorTechnician(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TechnicianId')
    Name = models.CharField(max_length=100, db_column='TechnicianName')
    Designation = models.CharField(max_length=100, db_column='Designation')
    StaffId = models.CharField(max_length=100, db_column='StaffId',unique=True)
    TerritoryId = models.ManyToManyField(Territory, db_column='TerritoryId')
    MobileNo = models.CharField(max_length=20, db_column='MobileNo')
    user = models.ForeignKey(User, db_column='SupervisorCode', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = 'Motor Technician'
        managed = False
        db_table = 'MotorTechnician'

class EngTarget(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TargetId')
    FreeService = models.IntegerField(db_column='FreeService', default=0, verbose_name='Free Service')
    PaidService = models.IntegerField(db_column='PaidService', default=0, verbose_name='Paid Service')
    WarrantyService = models.IntegerField(db_column='WarrantyService', default=0, verbose_name='Warranty Service')
    EntryDate = models.DateTimeField(db_column='EntryDate', auto_now_add=True, verbose_name='Date')
    EngUser = models.ForeignKey(User, related_name='EngTarget_EngUser', on_delete=models.CASCADE)
    EntryBy = models.ForeignKey(User, related_name='EngTarget_EntryBy', on_delete=models.CASCADE)

    def __str__(self):
        return self.EngUser.name

    class Meta:
        verbose_name_plural = 'Engineer Target'
        managed = False
        db_table = 'EngTarget'

class UserInfo(models.Model):
    Id = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    IsActive = models.ForeignKey(RowStatus, db_column='IsActive', on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_column='SupervisorId', on_delete=models.CASCADE)
    MotorTechnicianId = models.ForeignKey(MotorTechnician, db_column='MotorTechnicianId', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.UserName

    class Meta:
        managed = False
        db_table = 'TsaTsoLogin'

class TsaTarget(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TargetId')
    FreeService = models.IntegerField(db_column='FreeService', default=0)
    PaidService = models.IntegerField(db_column='PaidService', default=0)
    WarrantyService = models.IntegerField(db_column='WarrantyService', default=0)
    EntryDate = models.DateTimeField(db_column='EntryDate', auto_now_add=True, verbose_name='Date')
    TsaTsoUser = models.ForeignKey(UserInfo, db_column='EngUser', on_delete=models.CASCADE)
    EntryBy = models.ForeignKey(User, db_column='EntryBy', on_delete=models.CASCADE)

    def __str__(self):
        return self.TsaTsoUser.UserName

    class Meta:
        verbose_name_plural = 'TSA Target'
        managed = False
        db_table = 'TsaTarget'

class ServiceCallType(models.Model):
    Id = models.AutoField(primary_key=True)
    CallTypeName = models.CharField(max_length=50)

    def __str__(self):
        return self.CallTypeName

    class Meta:
        managed = False
        db_table = 'ServiceCallType'

class ServiceCategory(models.Model):
    Id = models.AutoField(primary_key=True, db_column='CategoryId')
    CategoryDetails = models.CharField(max_length=50, db_column='CategoryDetails')

    def __str__(self):
        return self.CategoryDetails

    class Meta:
        managed = False
        db_table = 'ServiceCategory'

class ServiceDetails(models.Model):
    Id = models.AutoField(primary_key=True, db_column='ServiceDetailsId')
    CustomerName = models.CharField(max_length=100, db_column='CustomerName', default='N/A')
    Mobile = models.CharField(max_length=20,db_column='Mobile', default='N/A')
    Chassis = models.CharField(max_length=100, db_column='KEY_CHASSIS', default='N/A')
    PurchaseDate = models.DateTimeField(db_column='PurchaseDate')
    DriverName = models.CharField(max_length=100, db_column='DriverName', default='N/A')
    DriverNumber = models.CharField(max_length=100, db_column='DriverNumber', default='N/A')
    HoursProvided = models.IntegerField(db_column='HoursProvided', default=0, verbose_name='Mileage')
    DateOfInstallation = models.DateTimeField(db_column='DateOfInstallation')

    ServiceDemandDate = models.DateTimeField(db_column='ServiceDemandDate')
    ServiceStartDate = models.DateTimeField(db_column='ServiceStartDate')
    ServiceEndDate = models.DateTimeField(db_column='ServiceEndDate')
    ServiceIncome = models.FloatField(db_column='ServiceIncome', default=0.0)
    VisitDate = models.DateTimeField(db_column='VisitDate')

    MobileCreatedDT = models.DateTimeField(db_column='MobileCreatedDT', auto_now_add=True)
    MobileEditedDT = models.DateTimeField(db_column='MobileEditedDT', auto_now_add=True)
    MobileLogCount = models.IntegerField(db_column='MobileLogCount',default=0)
    MobileId = models.IntegerField(db_column='MobileId', default=0)
    ServerInsertDateTime = models.DateTimeField(auto_now_add=True)
    ServerUpdateDateTime = models.DateTimeField(auto_now=True)

    ServiceRatting = models.CharField(db_column='ServiceRatting', max_length=20, default='0')
    IsVerify = models.ForeignKey(RowStatus, db_column='IsVerify', on_delete=models.CASCADE)

    UserId = models.ForeignKey(UserInfo, db_column='UserId', on_delete=models.CASCADE)
    ServiceCategoryId = models.ForeignKey(ServiceCategory, db_column='ServiceCategoryId', on_delete=models.CASCADE)
    ServiceCallTypeId = models.ForeignKey(ServiceCallType, db_column='ServiceCallTypeId', on_delete=models.CASCADE)
    SupervisorCode = models.ForeignKey(User, db_column='SupervisorCode', on_delete=models.CASCADE)


    def __str__(self):
        return self.CustomerName

    class Meta:
        verbose_name_plural = 'Service Details'
        managed = False
        db_table = 'ServiceDetails'