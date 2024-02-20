"""
   dashboard views file
"""

# django import
import json
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

# local import
from apps.dashboard.serializers import MenuListSerializer, ProjectSerializer, CapabilitySerializer, \
    SubCapabilitySerializer, SuccessReportSerializer, SuccessReportSerializer1
from ..accounts.permissions import IFSPermission
from ..utility.create_success_report import success_report, convert_json, all_list
from ..utility.get_create_report import create_report
from ..utility.issue_listing import issue_list_data
from ..utility.issue_details import issue_details_data
from apps.dashboard.models.masters import (MenuCardMaster, ProjectMaster, CapabilityMaster, SubCapabilityMaster,
                                           SDMMaster, SdoMaster, CSMMaster)
from apps.dashboard.models.models import SuccessReport


def get_issue_list(request):
    """
    used to fetch all issues
    """
    if request.method == 'GET':
        response, total_record = issue_list_data(request)
        return JsonResponse({'resdata': response, 'total_record': total_record, 'status': status.HTTP_200_OK})
    else:
        return JsonResponse({'error': 'something went wrong', 'status': status.HTTP_400_BAD_REQUEST})


def get_issue_details(request,id):
    """
    used to fetch specific issue
    """
    if request.method == 'GET':
        response = issue_details_data(request,id)
        return JsonResponse({'resdata': response, 'status': status.HTTP_200_OK})
    else:
        return JsonResponse({'error': 'something went wrong', 'status': status.HTTP_400_BAD_REQUEST})


def get_create_report(request, id):
    """
    used to fetch specific issue
    """
    if request.method == 'GET':
        response = SuccessReport.objects.filter(jira_key=id).first()
        menu_card, product, capability = all_list()
        if not response:
            response = create_report(request, id)
            response['menu_card_list'] = menu_card
            response['product_list'] = product
            response['capability_list'] = capability
        else:
            response = {
                "issue_key": response.jira_key,
                "menu_card": response.menu_card.menu_card,
                "capability": response.capability.capability_name,
                "product": response.product.product_name,
                "project_name": response.product.product_name,
                "snow_case_no": response.snow_case_no,
                "creator_email": response.creator.creator_email,
                "assignee_name": "Andreas Andersson",
                "creator_name": response.creator.creator_name,
                "report_status": response.report_status.report_status_name,
                "menu_card_list": menu_card,
                "product_list": product,
                "capability_list": capability,
            }
        return JsonResponse({'resdata': response, 'status': status.HTTP_200_OK})
    else:
        return JsonResponse({'error': 'something went wrong', 'status': status.HTTP_400_BAD_REQUEST})


class MenuViewSet(viewsets.ModelViewSet):
    """
    menu card view set, used to get menu list and specific record
    """
    queryset = MenuCardMaster.objects.all()
    serializer_class = MenuListSerializer

    def list(self, request, *args, **kwargs):
        """
        get menu card list
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'resdata': serializer.data, 'status': status.HTTP_200_OK})

    def retrieve(self, request, *args, **kwargs):
        """
        get menu card details
        """
        instance = self.get_queryset().filter(id=kwargs.get('pk')).first()
        serializer = self.get_serializer(instance)
        return Response({'resdata': serializer.data, 'status': status.HTTP_200_OK})


class ProjectViewSet(viewsets.ModelViewSet):
    """
    project view set, used to get project list
    """
    queryset = ProjectMaster.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        """
        get project list
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'resdata': serializer.data, 'status': status.HTTP_200_OK})


class CapabilityViewSet(viewsets.ModelViewSet):
    """
    capability view set, used to get, create, retrieve, update and delete capability
    """
    queryset = CapabilityMaster.objects.all()
    serializer_class = CapabilitySerializer

    def create(self, request, *args, **kwargs):
        """
        create capability
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Capability created successfully', 'status': status.HTTP_201_CREATED})
        return Response({'message': 'Something went wrong', 'status': status.HTTP_400_BAD_REQUEST})


class SubCapabilityViewSet(viewsets.ModelViewSet):
    """
    sub capability view set, used to get, create, retrieve, update and delete sub capability
    """
    queryset = SubCapabilityMaster.objects.all()
    serializer_class = SubCapabilitySerializer

    def list(self, request, *args, **kwargs):
        """
        get sub capability list
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK})

    def create(self, request, *args, **kwargs):
        """
        create sub-capability object
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'SubCapability created successfully', 'status': status.HTTP_201_CREATED})
        return Response({'message': 'Something went wrong', 'status': status.HTTP_400_BAD_REQUEST})


class IssueViewSet(viewsets.ModelViewSet):
    pass


class SuccessReportViewSet(viewsets.ModelViewSet):
    """
    success-report view set, used to create report
    """
    queryset = SuccessReport.objects.all()
    serializer_class = SuccessReportSerializer
    permission_classes = [IFSPermission]

    def create(self, request, *args, **kwargs):
        """
        create report
        """
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response({'msg': 'success-report created successfully!', 'status': status.HTTP_201_CREATED})

    def update(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(id=kwargs.get('pk')).first()
        if instance is not None:
            serializer = self.get_serializer_class()(instance, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response({'msg': 'success-report updated successfully!', 'status': status.HTTP_200_OK})
        return Response({'msg': 'Not Found', 'status': status.HTTP_404_NOT_FOUND})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(id=kwargs.get('pk')).first()
        serializer = self.get_serializer_class()(instance)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK})


class SuccessReportViewSet1(viewsets.GenericViewSet):
    serializer_class = SuccessReportSerializer1

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            response = success_report(serializer.validated_data)
            return Response({'data': convert_json(response[0]), 'status': status.HTTP_201_CREATED})
        return Response({'msg': 'something went wrong', 'status': status.HTTP_404_NOT_FOUND})

