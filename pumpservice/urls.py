from rest_framework import routers
from .views import *


from django.conf.urls import url, include

router = routers.DefaultRouter()
router.register(r'login', LoginViewSet)
router.register(r'manageservice', ServiceDetailsViewSet)
router.register(r'getuserservice', GetUserServiceViewSet)
# router.register(r'getcustomerdetail', GetCustomerDetail)
#router.register(r'servicelistbytsa', ServiceListByTsa)

urlpatterns = [
    url(r'^', include(router.urls)),
]