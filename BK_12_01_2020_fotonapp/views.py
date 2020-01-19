from django.shortcuts import render

from rest_framework import viewsets, filters
#from rest_framework.decorators import detail_route, list_route
#from rest_framework.views import APIView
import os
from rest_framework.response import Response
from datetime import datetime
from .models import *
from rest_framework.reverse import reverse
from .serializer import *
import json
import pyodbc

# Create your views here.
class LoginViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    def create(self, request):
        user = request.POST['Username']
        pwd = request.POST['Password']
        obj = UserInfo.objects.filter(UserName = str(user), Password = str(pwd))
        if len(list(obj.values())) > 0:
            response = {'StatusCode': '200', 'StatusMessage': 'Login Successful'}
        else:
            response = {'StatusCode': '400', 'StatusMessage': 'Bad request. Login credentials are not valid'}
        return Response(response)


class ServiceDetailsViewSet(viewsets.ModelViewSet):
    queryset = ServiceDetails.objects.all()
    serializer_class = ServiceDetailsSerializer

    def create(self, request):
        try:
            mobileIdSynch = list()
            userid = str(request.data.get('UserId'))
            data = json.loads(request.data.get('Data'))
            print(data)
            print(userid)
            for elem in data:
                #print("----AAAA----"+str(elem))
                TractorPurchaseDate = datetime.strptime(str(elem['KEY_BUYING_DATE']), '%Y-%m-%d %H:%M:%S')
                DateOfInstallation = datetime.strptime(str(elem['KEY_INSTALLAION_DATE']), '%Y-%m-%d %H:%M:%S')
                ServiceDemandDate = datetime.strptime(str(elem['KEY_CALL_SERVICE_DATE']), '%Y-%m-%d %H:%M:%S')
                ServiceStartDate = datetime.strptime(str(elem['KEY_SERVICE_START_DATE']), '%Y-%m-%d %H:%M:%S')
                ServiceEndDate = datetime.strptime(str(elem['KEY_SERVICE_END_DATE']), '%Y-%m-%d %H:%M:%S')
                VisitDate = datetime.strptime(str(elem['KEY_VISITED_DATE']), '%Y-%m-%d %H:%M:%S')
                MobileCreatedDT = datetime.strptime(str(elem['KEY_CREATED_AT']), '%Y-%m-%d %H:%M:%S')
                MobileEditedDT = datetime.strptime(str(elem['KEY_EDITED_AT']), '%Y-%m-%d %H:%M:%S')
                MobileId = int(elem['KEY_ID'])

                user_key = UserInfo.objects.filter(UserName=userid).first()
                service_category_key = ServiceCategory.objects.filter(pk=int(elem['KEY_SERVICE_TYPE'])).first()
                service_call_key = ServiceCallType.objects.filter(pk=int(elem['KEY_CALL_TYPE'])).first()

                data_mobile = ServiceDetails.objects.filter(MobileId=MobileId, UserId=user_key)

                if len(list(data_mobile.values())) > 0: #Update operation
                    data_mobile = data_mobile[0]
                    data_mobile.CustomerName = str(elem['KEY_CUSTOMER_NAME'])
                    data_mobile.Mobile = str(elem['KEY_CUSTOMER_MOBILE'])
                    data_mobile.Chassis = str(elem['KEY_CHASSIS']),
                    data_mobile.PurchaseDate = datetime.strptime(str(elem['KEY_BUYING_DATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.HoursProvided = int(elem['KEY_RUNNING_HOUER'])
                    data_mobile.DateOfInstallation = datetime.strptime(str(elem['KEY_INSTALLAION_DATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.DriverName = str(elem['KEY_DRIVER_NAME']),
                    data_mobile.DriverNumber = str(elem['KEY_DRIVER_NUMBER']),
                    data_mobile.ServiceDemandDate = datetime.strptime(str(elem['KEY_CALL_SERVICE_DATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.ServiceStartDate = datetime.strptime(str(elem['KEY_SERVICE_START_DATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.ServiceEndDate = datetime.strptime(str(elem['KEY_SERVICE_END_DATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.ServiceIncome = float(elem['KEY_SERVICE_INCOME'])
                    data_mobile.VisitDate = datetime.strptime(str(elem['KEY_VISITED_DATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.MobileCreatedDT = datetime.strptime(str(elem['KEY_CREATED_AT']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.MobileEditedDT = datetime.strptime(str(elem['KEY_EDITED_AT']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.MobileLogCount = int(elem['KEY_EDIT_LOG_COUNT'])
                    data_mobile.ServiceRatting = str(elem['KEY_RATING'])
                    data_mobile.MobileId = MobileId
                    data_mobile.UserId = user_key
                    data_mobile.ServiceCategoryId = service_category_key
                    data_mobile.CallTypeId = service_call_key
                    data_mobile.save()
                    #mobileIdSynch.append(MobileId)
                else:
                    #print("----BBBBB----" + str(elem))
                    supeCode = MotorTechnician.objects.filter(StaffId=str(userid)).values('user').first()
                    supervisorCode = User.objects.filter(pk=int(supeCode['user'])).first()
                    isVerify = RowStatus.objects.filter(pk=int(2)).first()
                    obj = ServiceDetails(CustomerName=str(elem['KEY_CUSTOMER_NAME']),
                                         Mobile=str(elem['KEY_CUSTOMER_MOBILE']),
                                         Chassis=str(elem['KEY_CHASSIS']),
                                         PurchaseDate=TractorPurchaseDate,
                                         HoursProvided=int(elem['KEY_RUNNING_HOUER']),
                                         DateOfInstallation=DateOfInstallation,
                                         DriverName=str(elem['KEY_DRIVER_NAME']),
                                         DriverNumber=str(elem['KEY_DRIVER_NUMBER']),
                                         ServiceDemandDate=ServiceDemandDate,
                                         ServiceStartDate=ServiceStartDate,
                                         ServiceEndDate=ServiceEndDate,
                                         ServiceIncome=float(elem['KEY_SERVICE_INCOME']),
                                         VisitDate=VisitDate,

                                         MobileCreatedDT=MobileCreatedDT,
                                         MobileEditedDT=MobileEditedDT,
                                         MobileLogCount=int(elem['KEY_EDIT_LOG_COUNT']),
                                         MobileId=MobileId,

                                         ServiceRatting=str(elem['KEY_RATING']),
                                         IsVerify=isVerify,
                                         UserId=user_key,

                                         ServiceCategoryId=service_category_key,
                                         ServiceCallTypeId=service_call_key,
                                         SupervisorCode=supervisorCode)

                    obj.save()
                    #mobileIdSynch.append(MobileId)

            return Response({'StatusCode': '200', 'StatusMessage': 'Service Added Successfully'})
        except Exception as ex:
            return Response({'StatusCode': '500', 'StatusMessage': 'Exception Occured. Details: ' + str(ex)})


class GetUserServiceViewSet(viewsets.ModelViewSet):
    queryset = ServiceDetails.objects.all()
    serializer_class = ServiceDetailsSerializer
    def create(self, request):
        try:
            userid = str(request.data.get('UserId'))
            user_key = UserInfo.objects.filter(UserName=userid).first()
            obj = ServiceDetails.objects.filter(UserId=user_key).order_by('MobileId')
            data = list(obj.values())
            return Response({'StatusCode': '200', 'StatusMessage': data})
        except Exception as ex:
            return Response({'StatusCode': '500', 'StatusMessage': 'Exception Occured. Details: ' + str(ex)})

class GetCustomerDetail(viewsets.ModelViewSet):
    queryset = ServiceDetails.objects.all()
    serializer_class = ServiceDetailsSerializer

    def create(self, request):
        try:
            chessisNo = str(request.data.get('ChassisNo'))

            conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                  "Server=192.168.100.25;"
                                  "Database=FOTON;"
                                  "Trusted_Connection=no;"
                                  "UID=sa;"
                                  "PWD=dataport;")
            cursor = conn.cursor()
            cursor.execute("SELECT TOP 1 Cstm.CustomerCode, Cstm.CustomerName1, Cstm.Mobile, Inv.InvoiceDate "
                           "FROM [FOTON].[dbo].[InvoiceDetailsBatch] InvDtl "+
                           "INNER JOIN Invoice Inv ON InvDtl.Invoiceno = Inv.InvoiceNo "+
                           "INNER JOIN Customer Cstm ON Cstm.CustomerCode = Inv.CustomerCode "+
                           "WHERE InvDtl.BatchNo = '"+chessisNo+"'")
            record = cursor.fetchone()
            cursor.close()
            conn.close()
            StatusCode = ''
            customerName=record[1]
            customerMobile=record[2]
            invoiceDate=record[3]

            jDict = {'customerName':record[1],'customerMobile':record[2],'invoiceDate':record[3]}

            if record:
                StatusCode = '200'
                data = jDict
            else:
                StatusCode = '201'
                data = 'No Data Found.'

            return Response({'StatusCode': StatusCode, 'StatusMessage': data})
        except Exception as ex:
            return Response({'StatusCode': '500', 'StatusMessage': 'Exception Occured. Details: ' + str(ex)})

