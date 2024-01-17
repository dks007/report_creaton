import json
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.dashboard.serializers import MenuListSerializer, ProjectSerializer, CapabilitySerializer, \
    SubCapabilitySerializer, SuccessReportSerializer
from ..utility.issue_listing import issue_list_data
from ..utility.issue_details import issue_details_data
from apps.dashboard.models.masters import (MenuCardMaster, ProjectMaster, CapabilityMaster, SubCapabilityMaster,
                                           SDMMaster, SdoMaster, CSMMaster)
from apps.dashboard.models.models import SuccessReport


# Add any additional views or custom logic as needed
def get_issue_list(request):
    if request.method == 'GET':
        # response = issue_list_data()
        response = issue_list_data()
        # print(response)
        # print(response,'>>>>>>>>>')
        response = json.loads(response)

        for dt in response:
            desc = MenuCardMaster.objects.filter(menu_card=dt.get('menu_card')).first()
            report_status = SuccessReport.objects.filter(jira_key=dt.get('issue_key')).first()
            if report_status:
                dt['status'] = report_status.report_status.report_status_name
            else:
                dt['status'] = 'Not Created'
            if desc is not None:
                dt['menu_description'] = desc.menu_description
        return JsonResponse({'data': response, 'status': status.HTTP_200_OK})
    else:
        return JsonResponse({'error': 'something went wrong', 'status': status.HTTP_400_BAD_REQUEST})


def get_issue_details(request, id):
    if request.method == 'GET':
        response = issue_details_data(id)
        return JsonResponse({'data': response, 'status': status.HTTP_200_OK})
    else:
        return JsonResponse({'error': 'something went wrong', 'status': status.HTTP_400_BAD_REQUEST})


class MenuViewSet(viewsets.ModelViewSet):
    queryset = MenuCardMaster.objects.all()
    serializer_class = MenuListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(id=kwargs.get('pk')).first()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = ProjectMaster.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK})


class CapabilityViewSet(viewsets.ModelViewSet):
    queryset = CapabilityMaster.objects.all()
    serializer_class = CapabilitySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Capability created successfully', 'status': status.HTTP_201_CREATED})
        return Response({'message': 'Something went wrong', 'status': status.HTTP_400_BAD_REQUEST})


class SubCapabilityViewSet(viewsets.ModelViewSet):
    queryset = SubCapabilityMaster.objects.all()
    serializer_class = SubCapabilitySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'data': serializer.data, 'status': status.HTTP_200_OK})

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'SubCapability created successfully', 'status': status.HTTP_201_CREATED})
        return Response({'message': 'Something went wrong', 'status': status.HTTP_400_BAD_REQUEST})


class IssueViewSet(viewsets.ModelViewSet):
    pass


class SuccessReportViewSet(viewsets.ModelViewSet):
    queryset = SuccessReport.objects.all()
    serializer_class = SuccessReportSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response({'msg': 'success-report created successfully!', 'status': status.HTTP_201_CREATED})
