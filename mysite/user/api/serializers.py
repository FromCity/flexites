from rest_framework import serializers

from ..models import Organization, User

class OrganizationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    organizations = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    @staticmethod
    def get_organizations(obj):
        return OrganizationsSerializer(Organization.objects.filter(id__in=User.objects.filter(email=obj.email).values('organizations')), many=True).data

