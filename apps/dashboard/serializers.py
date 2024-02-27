# dashboard/serializers.py
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import base64

from apps.dashboard.models import SuccessReport
from apps.dashboard.models.masters import (MenuCardMaster, CustomerMaster, ProjectMaster, CapabilityMaster, SubCapabilityMaster,
                                           CreatorMaster, ExpertMaster, LogoMaster, CustomerContactMaster)


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
        #fields = '__all__'
        fields = ['id', 'product_name']

class CustomerContactSerializer(serializers.ModelSerializer):
    """
    customer contact serializer, used to serialize all project objects
    """
    class Meta:
        model = CustomerContactMaster
        #fields = '__all__'
        fields = ['id', 'customer_contact']

class CustomerSerializer(serializers.ModelSerializer):
    """
    customer  serializer, used to serialize all project objects
    """
    class Meta:
        model = CustomerMaster
        #fields = '__all__'
        fields = ['id', 'customer_name']

class CapabilitySerializer(serializers.ModelSerializer):
    """
    capability serializer, used to serialize all capability objects
    """
    class Meta:
        model = CapabilityMaster
        #fields = '__all__'
        fields = ['id', 'capability_name']

class SubCapabilitySerializer(serializers.ModelSerializer):
    """
    sub-capability serializer, used to serialize all sub-capability objects
    """
    class Meta:
        model = SubCapabilityMaster
        fields = ['id', 'sub_capability_name']


class ExpertSerializer(serializers.ModelSerializer):
    """
    expert serializer, used to serialize expert objects
    """
    class Meta:
        model = ExpertMaster
        fields = ['id', 'expert_name']
        #fields = ('expert_name',)

class MenuCardSerializer(serializers.ModelSerializer):
    """
    expert serializer, used to serialize expert objects
    """
    class Meta:
        model = MenuCardMaster
        fields = ['id', 'menu_card']
        #fields = ('expert_name',)

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
        def get_logo(self, obj):
            if obj.logo:
                return base64.b64encode(obj.logo).decode('utf-8')
            return None
        fields = ('logo_file_name', 'logo_file_size', 'logo_url', 'status','logo')


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


class SuccessCreateReportSerializer(serializers.Serializer):
    """
    success-report serializer, used to serializer success-report objects,
    """
    issue_key = serializers.CharField(max_length=20, required=True)
    parent_key = serializers.CharField(max_length=20)
    menu_card = serializers.CharField(max_length=20)
    capability = serializers.CharField(max_length=100)
    product = serializers.CharField(max_length=100)
    expert_name = serializers.CharField(max_length=100)
    customer_name = serializers.CharField(max_length=100)
    project_name = serializers.CharField(max_length=100)
    snow_case_no = serializers.CharField(max_length=100)
    sdm_name = serializers.CharField(max_length=100)
    csm_name = serializers.CharField(max_length=100)
    sdo_name = serializers.CharField(max_length=100)
    #creator_email = serializers.CharField(max_length=100)
    #creator_name = serializers.CharField(max_length=100)
    customer_contact = serializers.CharField(max_length=100)
    action = serializers.CharField(max_length=20, required=True)
    # New field for logo file upload
    #logo = serializers.ImageField(required=True)
    #logo_url = serializers.CharField(max_length=100)

    def validate_logo(self, value):
        # Validate image file format
        if value:
            format = value.content_type.split('/')[1]
            if format not in ['jpeg', 'jpg', 'png']:
                raise ValidationError("Only JPEG and PNG formats are allowed for the logo.")
        return value
