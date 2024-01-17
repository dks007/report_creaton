# dashboard/serializers.py
from rest_framework import serializers

from apps.dashboard.models import SuccessReport
from apps.dashboard.models.masters import MenuCardMaster, ProjectMaster, CapabilityMaster, SubCapabilityMaster, \
    CreatorMaster, ExpertMaster


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


class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertMaster
        fields = ('expert_name',)


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatorMaster
        fields = ('creator_name',)


class SuccessReportSerializer(serializers.ModelSerializer):
    creator = CreatorSerializer()
    expert = ExpertSerializer()

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

