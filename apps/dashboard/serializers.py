# dashboard/serializers.py
from rest_framework import serializers

from apps.dashboard.models import SuccessReport
from apps.dashboard.models.masters import (MenuCardMaster, ProjectMaster, CapabilityMaster, SubCapabilityMaster,
                                           CreatorMaster, ExpertMaster, LogoMaster)


class MenuListSerializer(serializers.ModelSerializer):
    """
    menu list serializer, used to serialize all menu cards object
    """
    class Meta:
        model = MenuCardMaster
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    """
    project serializer, used to serialize all project objects
    """
    class Meta:
        model = ProjectMaster
        fields = '__all__'


class CapabilitySerializer(serializers.ModelSerializer):
    """
    capability serializer, used to serialize all capability objects
    """
    class Meta:
        model = CapabilityMaster
        fields = '__all__'


class SubCapabilitySerializer(serializers.ModelSerializer):
    """
    sub-capability serializer, used to serialize all sub-capability objects
    """
    class Meta:
        model = SubCapabilityMaster
        fields = '__all__'


class ExpertSerializer(serializers.ModelSerializer):
    """
    expert serializer, used to serialize expert objects
    """
    class Meta:
        model = ExpertMaster
        fields = ('expert_name',)


class CreatorSerializer(serializers.ModelSerializer):
    """
    creator serializer, used to serialize creator objects
    """
    class Meta:
        model = CreatorMaster
        fields = ('creator_name',)


class LogoSerializer(serializers.ModelSerializer):
    """
    logo serializer, used to serialize logo objects
    """
    class Meta:
        model = LogoMaster
        fields = ('logo_file_name', 'logo_file_size', 'logo_url', 'status')


class SuccessReportSerializer(serializers.ModelSerializer):
    """
    success-report serializer, used to serializer success-report objects,
    """
    creator = CreatorSerializer()
    expert = ExpertSerializer()
    logo = LogoSerializer()

    class Meta:
        model = SuccessReport
        fields = ("jira_key", "menu_card", "customer", "expert", "product", "capability", "sub_capability",
                  "logo", "status", "creator", "created_by", "updated_by", "report_status")

    def create(self, validated_data):
        creator = CreatorMaster.objects.filter(creator_name=validated_data['creator']['creator_name']).first()
        expert = ExpertMaster.objects.filter(expert_name=validated_data['expert']['expert_name']).first()
        validated_data['expert'] = expert
        validated_data['creator'] = creator
        return super().create(validated_data)
