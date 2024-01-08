# dashboard/serializers.py
from rest_framework import serializers
from apps.dashboard.models.masters import MenuCardMaster, ProjectMaster, CapabilityMaster, SubCapabilityMaster


class MenuListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuCardMaster
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectMaster
        fields = '__all__'


class CapabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = CapabilityMaster
        fields = '__all__'


class SubCapabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCapabilityMaster
        fields = '__all__'
