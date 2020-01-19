from django.contrib import admin

from django import forms
from django.contrib import admin
from .models import  *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django.core.exceptions import ValidationError
from django.conf.urls import url,include
import datetime
#from django.conf.urls.defaults import *
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.html import format_html
import csv
from django.contrib import messages

from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

admin.site.site_header = "Foton Service Administration"
admin.site.site_title = "Foton Service"
admin.site.index_title = "Foton Service"

admin.site.register(Territory)

class AreaAdmin(admin.ModelAdmin):
    filter_horizontal = ['TerritoryId']

admin.site.register(Area,AreaAdmin)

class UserAreaAdmin(admin.ModelAdmin):
    filter_horizontal = ['AreaId']
admin.site.register(UserArea, UserAreaAdmin)
admin.site.unregister(User)

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name' , 'last_name', )

class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    #filter_horizontal = ['AreaId']
    prepopulated_fields = {'username': ('first_name' , 'last_name', )}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'password1', 'password2', 'groups','is_staff' ),
        }),
    )

admin.site.register(User, UserAdmin)

class MotorTechnicianAdmin(admin.ModelAdmin):
    #list_display = ('Name', 'Designation','StaffId', 'TerritoryCode','MobileNo')
    list_display = ('Name', 'Designation', 'StaffId', 'MobileNo')
    search_fields = ['Name', 'StaffId', 'MobileNo']
    list_filter = ['StaffId', 'MobileNo']
    filter_horizontal = ['TerritoryId']
    ordering = ['-Id']
    list_per_page = 20

    def get_queryset(self, request):
        if request.user.id == 1:
            qs = super(MotorTechnicianAdmin, self).get_queryset(request)
            return qs.all()
        else:
            qs = super(MotorTechnicianAdmin, self).get_queryset(request)
            return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        tsaUser = UserInfo.objects.filter(MotorTechnicianId=obj).first()
        if not tsaUser:
            rowStatus = RowStatus.objects.filter(pk=int(1)).first()
            UserInfo(UserName=str(obj.StaffId), Password=str(obj.StaffId), IsActive=rowStatus, user=request.user, MotorTechnicianId=obj).save()
        else :
            UserInfo.objects.filter(MotorTechnicianId=obj).update(UserName=str(obj.StaffId), Password=str(obj.StaffId))
        #return super(MotorTechnicianAdmin, self).save_model(request, obj, form, change)

        return obj

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("user",)
        form = super(MotorTechnicianAdmin, self).get_form(request, obj, **kwargs)
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "TerritoryId":
            aList = UserArea.objects.filter(UserId=request.user).values_list('AreaId__Id', flat=True)
            uAreaList = Area.objects.filter(id__in=aList).values_list('TerritoryId__Id',flat=True )
            kwargs["queryset"] = Territory.objects.filter(pk__in=uAreaList)
        return super(MotorTechnicianAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MotorTechnician, MotorTechnicianAdmin)

class EngTargetAdmin(admin.ModelAdmin):
    list_display = ('FreeService', 'PaidService', 'WarrantyService', 'EntryDate', 'EngUser')
    search_fields = ['EngUser']
    #list_filter = ['EngUser']
    list_filter = (
        ('EntryDate', DateRangeFilter),
    )
    ordering = ['-Id']
    list_per_page = 20

    def queryset(self, request, queryset):
        if request.user.id == 1:
            return queryset.objects.all()
        else:
            return queryset.filter(EngUser__id=int(request.user))

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("EntryBy",)
        form = super(EngTargetAdmin, self).get_form(request, obj, **kwargs)
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "EngUser":
            kwargs["queryset"] = User.objects.filter(groups__name='Engineer')
        return super(EngTargetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        tempEntryDate = obj.EntryDate
        fObje = EngTarget.objects.filter(EngUser=obj.EngUser, EntryDate__month=tempEntryDate.month,
                                    EntryDate__year=tempEntryDate.year)
        if fObje:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "For this Engineer target already exists in this month.")
            return
        else:
            return super(EngTargetAdmin, self).save_model(request, obj, form, change)


admin.site.register(EngTarget, EngTargetAdmin)


class TsaTargetAdmin(admin.ModelAdmin):
    list_display = ('FreeService', 'PaidService', 'WarrantyService', 'EntryDate', 'TsaTsoUser')
    search_fields = ['TsaTsoUser']
    list_filter = (
        ('EntryDate', DateRangeFilter),'TsaTsoUser'
    )
    ordering = ['-Id']
    list_per_page = 20


    def save_model(self, request, obj, form, change):
        tempEntryDate = obj.EntryDate

        engTargObje = EngTarget.objects.filter(EngUser=request.user, EntryDate__month=tempEntryDate.month,
                                         EntryDate__year=tempEntryDate.year)
        if not engTargObje:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "Your Target yest not set. Please contact system Admin.")
            return
        else:
            fObje = TsaTarget.objects.filter(TsaTsoUser=obj.TsaTsoUser, EntryDate__month=tempEntryDate.month,
                                        EntryDate__year=tempEntryDate.year)
            if fObje:
                messages.set_level(request, messages.ERROR)
                messages.error(request, "For this TSA/TSO target already exists in this month.")
                return
            else:
                return super(TsaTargetAdmin, self).save_model(request, obj, form, change)


    def queryset(self, request, queryset):
        if request.user.id == 1:
            return queryset.objects.all()
        else:
            return queryset.filter(EntryBy__id=int(request.user))

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("EntryBy",)
        form = super(TsaTargetAdmin, self).get_form(request, obj, **kwargs)
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "TsaTsoUser":
            kwargs["queryset"] = MotorTechnician.objects.filter(user=request.user)
        return super(TsaTargetAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(TsaTarget, TsaTargetAdmin)

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow(field_names)
        with open('foronapp.servicedetails', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(response, delimiter=',')
            for obj in queryset:
                row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class ServiceDetailsAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('UserId', 'ServerInsertDateTime', 'CustomerName', 'Mobile', 'HoursProvided', 'ServiceCategoryId', 'ServiceCallTypeId')
    search_fields = ['CustomerName', 'Mobile']
    actions = ["export_as_csv"]
    readonly_fields = ['CustomerName', 'Mobile', 'Chassis', 'PurchaseDate', 'HoursProvided',
              'DateOfInstallation', 'ServiceDemandDate','ServiceStartDate',
              'ServiceEndDate', 'ServiceIncome', 'VisitDate', 'UserId',
              'ServiceCategoryId', 'ServiceCallTypeId']

    def changelist_view(self, request, extra_context=None):
        if request.user.id == 1:
            self.list_display = (
            'TechnicianName', 'CustomerName', 'Mobile', 'ServiceDemandDate', 'ServiceStartDate', 'ServiceEndDate')
        return super(ServiceDetailsAdmin, self).changelist_view(request, extra_context)

    list_filter = (
        ('ServiceDemandDate', DateRangeFilter), 'IsVerify', 'ServiceCategoryId', 'ServiceCallTypeId',
    )

    def TechnicianName(self, obj):
        staffId = UserInfo.objects.filter(UserName=obj.UserId).values('UserName').first()
        result = MotorTechnician.objects.filter(StaffId=staffId['UserName']).values('Name').first()

        return result.get('Name')

    ordering = ['-Id']
    list_per_page = 20
    fields = ('CustomerName', 'Mobile', 'Chassis', 'PurchaseDate', 'HoursProvided',
              'DateOfInstallation', 'ServiceDemandDate','ServiceStartDate',
              'ServiceEndDate', 'ServiceIncome', 'VisitDate', 'UserId',
              'ServiceCategoryId', 'ServiceCallTypeId', 'IsVerify')

    def queryset(self,request):
        if request.user.id == 1:
            qs = super(ServiceDetailsAdmin, self).get_queryset(request)
            return qs.all()
        else:
            qs = super(ServiceDetailsAdmin, self).get_queryset(request)
            return qs.filter(SupervisorCode=request.user)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("SupervisorCode",)
        return super(ServiceDetailsAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(ServiceDetails, ServiceDetailsAdmin)