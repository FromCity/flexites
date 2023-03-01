from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .pkg import save_photo
from mysite import settings
import uuid
from django.http import JsonResponse
from rest_framework.decorators import action
from os import path
import json
import jwt


from .serializers import (
    OrganizationsSerializer,
    UserSerializer
)

from ..models import Organization, User

class AllOrganizationsViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationsSerializer


class RegisterUser(APIView):

    def post(self, request):
        data_req = request.POST.get('data')
        data = json.loads(data_req)
        email = data['email']
        password = data['password']
        surname = data['surname']
        first_name = data['first_name']
        phone = data['phone']
        id_organizations = data['id_organizations']
        in_photo = request.FILES['file']
        in_photo_name = request.FILES['file'].name
        file_name = str(uuid.uuid1())
        extension = path.splitext(in_photo_name)[1]
        name_avatar = file_name + extension
        save_photo(
            in_photo=in_photo,
            file_name= path.join(str(settings.MEDIA_ROOT), 'images', name_avatar),
            size=(200, 200))
        User.objects.create(
            email = email,
            password = password,
            surname = surname,
            first_name = first_name,
            phone = phone,
            photo = 'images/'+name_avatar)
        for id_org in id_organizations:
            User.objects.get(email=email).organizations.add(id_org)
        response = {'email': email}
        return Response(status=200, data=response)


class AllUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EditUser(APIView):

    def post(self, request):
        encoded_jwt =request.POST.get('token')
        payload = jwt.decode(encoded_jwt, 'secret', algorithms=["HS256"])
        id_auth = payload["email"]
        data_req = request.POST.get('data')
        data = json.loads(data_req)
        email = data['email']
        password = data['password']
        surname = data['surname']
        first_name = data['first_name']
        phone = data['phone']
        id_organizations = data['id_organizations']
        try:
            in_photo = request.FILES['file']
        except:
            in_photo = None
        u = User.objects.get(id=id_auth)
        if in_photo:
            in_photo_name = request.FILES['file'].name
            file_name = str(uuid.uuid1())
            extension = path.splitext(in_photo_name)[1]
            name_avatar = file_name + extension
            save_photo(
                in_photo=in_photo,
                file_name= path.join(str(settings.MEDIA_ROOT), 'images', name_avatar),
                size=(200, 200))
            u.photo = 'images/'+name_avatar
        if email:
            u.email = email
        if password:
            u.password = password
        if surname:
            u.surname = surname
        if first_name:
            u.first_name = first_name
        if phone:
            u.phone = phone
        if id_organizations:
            for id_org in id_organizations:
                u.organizations.add(id_org)
        u.save()
        response = {'email': email}
        return Response(status=200, data=response)

class UserByID(APIView):


    def get(self, request):
        data_req = request.POST.get('data')
        data = json.loads(data_req)
        user_id = data['id']
        u = User.objects.filter(id=user_id).values()
        organizations = Organization.objects.filter(id__in=User.objects.filter(id=user_id).values('organizations')).values()

        return JsonResponse({"user": list(u), "organizations": list(organizations)})


class Login(APIView):


    def post(self, request):
        data_req = request.POST.get('data')
        data = json.loads(data_req)
        email = data['email']
        password = data['password']
        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            user = None
        if user:
            encoded_jwt = jwt.encode({"email": user.id}, "secret", algorithm="HS256")
            response = {'token': encoded_jwt, 'auth': "access"}
            return Response(status=200, data=response)
        else:
            response = {'auth': 'fail'}
            return Response(status=200, data=response)


class AddOrganization(APIView):


    def post(self, request):
        data_req = request.POST.get('data')
        data = json.loads(data_req)
        name = data['name']
        description = data['description']
        Organization.objects.create(name=name, description=description)
        return JsonResponse({"name": name})
