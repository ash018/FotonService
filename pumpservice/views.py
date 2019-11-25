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

class LoginViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = UserInfoSerializer

    def create(self, request):
        user = request.POST['Username']
        pwd = request.POST['Password']
        obj = AppUser.objects.filter(UserName = str(user), Password = str(pwd)).using('PumpTrack')
        if len(list(obj.values())) > 0:
            response = {'StatusCode': '200', 'StatusMessage': 'Login Successful'}
        else:
            response = {'StatusCode': '400', 'StatusMessage': 'Bad request. Login credentials are not valid'}
        return Response(response)


class ServiceDetailsViewSet(viewsets.ModelViewSet):
    queryset = ServiceDetails.objects.all().using('PumpTrack')
    serializer_class = ServiceDetailsSerializer

    def create(self, request):
        print("------======-----"+str(request))
        try:
            userid = str(request.data.get('UserId'))
            data = json.loads(request.data.get('Data'))
            print("----AAAA----" + str(data))
            for elem in data:
                print("----AAAA----"+str(data))
                ServiceDemandDate = datetime.strptime(str(elem['KEY_COMPLAINDATE']), '%Y-%m-%d %H:%M:%S')
                ServiceStartDate = datetime.strptime(str(elem['KEY_ATTENDATE']), '%Y-%m-%d %H:%M:%S')
                VisitDate = datetime.strptime(str(elem['KEY_ATTENDATE']), '%Y-%m-%d %H:%M:%S')
                MobileId = int(elem['KEY_ID'])

                user_key = AppUser.objects.filter(UserName=userid).first().using('PumpTrack')
                data_mobile = ServiceDetails.objects.filter(MobileId=MobileId, UserId=user_key).using('PumpTrack')

                if len(list(data_mobile.values())) > 0: #Update operation
                    data_mobile = data_mobile[0]
                    data_mobile.CustomerName = str(elem['KEY_CUSTOMERNAME'])
                    data_mobile.CustomerCode = str(elem['KEY_CUSTOMERCODE'])
                    data_mobile.Mobile = str(elem['KEY_MOBILENO'])
                    data_mobile.ServicePortFolio = str(elem['KEY_PORTFOLIO'])
                    data_mobile.ServiceCount = int(elem['KEY_SERVICETIME']),
                    data_mobile.ServiceDemandDate = datetime.strptime(str(elem['KEY_COMPLAINDATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.ServiceStartDate = datetime.strptime(str(elem['KEY_ATTENDATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.ServiceIncome = float(elem['KEY_SERVICECHARGE'])
                    data_mobile.VisitDate = datetime.strptime(str(elem['KEY_ATTENDATE']), '%Y-%m-%d %H:%M:%S')
                    data_mobile.MobileId = MobileId
                    data_mobile.UserId = user_key
                    data_mobile.save().using('PumpTrack')
                    #mobileIdSynch.append(MobileId)
                else:
                    obj = ServiceDetails(CustomerName=str(elem['KEY_CUSTOMERNAME']),
                                         CustomerCode=str(elem['KEY_CUSTOMERCODE']),
                                         Mobile=str(elem['KEY_MOBILENO']),
                                         ServicePortFolio=str(elem['KEY_PORTFOLIO']),
                                         ServiceCount=str(elem['KEY_SERVICETIME']),
                                         ProductModel=str(elem['KEY_MODEL']),

                                         ServiceDemandDate=ServiceDemandDate,
                                         ServiceStartDate=ServiceStartDate,
                                         #ServiceEndDate=ServiceEndDate,

                                         ServiceIncome=float(elem['KEY_SERVICECHARGE']),
                                         VisitDate=VisitDate,
                                         #MobileCreatedDT=MobileCreatedDT,
                                         #MobileEditedDT=MobileEditedDT,
                                         Latitude=float(elem['KEY_SLAT']),
                                         Longitude=float(elem['KEY_SLANG']),

                                         #MobileLogCount=int(elem['KEY_EDIT_LOG_COUNT']),
                                         MobileId=MobileId,
                                         #ServiceRatting=str(elem['KEY_RATING']),
                                         UserId=user_key)

                    obj.save().using('PumpTrack')

            return Response({'StatusCode': '200', 'StatusMessage': 'Service Added Successfully'})
        except Exception as ex:
            return Response({'StatusCode': '500', 'StatusMessage': 'Exception Occured. Details: ' + str(ex)})

class GetUserServiceViewSet(viewsets.ModelViewSet):
    queryset = ServiceDetails.objects.all().using('PumpTrack')
    serializer_class = ServiceDetailsSerializer
    def create(self, request):
        try:
            userid = str(request.data.get('UserId'))
            user_key = AppUser.objects.filter(UserName=userid).first().using('PumpTrack')
            obj = ServiceDetails.objects.filter(UserId=user_key).order_by('MobileId').using('PumpTrack')
            data = list(obj.values())
            return Response({'StatusCode': '200', 'StatusMessage': data})
        except Exception as ex:
            return Response({'StatusCode': '500', 'StatusMessage': 'Exception Occured. Details: ' + str(ex)})

