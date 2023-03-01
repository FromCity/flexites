from django.db import router
from django.urls import path

from rest_framework import routers
from .views import (
    AllOrganizationsViewSet, 
    RegisterUser, 
    AllUserViewSet, 
    EditUser,
    UserByID,
    Login,
    AddOrganization)

router = routers.SimpleRouter()
router.register('organizations', AllOrganizationsViewSet, basename='AllOrganizations')
router.register('users', AllUserViewSet, basename='AllUsers')

urlpatterns = [
    path('register', RegisterUser.as_view()),
    path('edit/user', EditUser.as_view()),
    path('user', UserByID.as_view()),
    path('login', Login.as_view()),
    path('add_organization', AddOrganization.as_view())
]

urlpatterns += router.urls