import json
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response

from apps.dashboard.serializers import MenuListSerializer, ProjectSerializer, CapabilitySerializer, \
    SubCapabilitySerializer
from ..utility.issue_listing import data
from ..utility.issue_details import specific_data
from apps.dashboard.models.masters import (MenuCardMaster, ProjectMaster, CapabilityMaster, SubCapabilityMaster,
                                           SDMMaster, SdoMaster, CSMMaster)


# Add any additional views or custom logic as needed
def access_data(request):
    if request.method == 'GET':
        response = data()
        response = json.loads(response)
        for dt in response:
            desc = MenuCardMaster.objects.filter(menu_card=dt.get('menu_card')).first()
            if desc is not None:
                dt['menu_description'] = desc.menu_description
        return JsonResponse({'data': response})


def access_specific_data(request, id):
    if request.method == 'GET':
        response = specific_data(id)
        return JsonResponse({'data': response})


class MenuViewSet(viewsets.ModelViewSet):
    queryset = MenuCardMaster.objects.all()
    serializer_class = MenuListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'data': serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(id=kwargs.get('pk')).first()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = ProjectMaster.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'data': serializer.data})


class CapabilityViewSet(viewsets.ModelViewSet):
    queryset = CapabilityMaster.objects.all()
    serializer_class = CapabilitySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Capability created successfully'})
        return Response({'message': 'Something went wrong'})


class SubCapabilityViewSet(viewsets.ModelViewSet):
    queryset = SubCapabilityMaster.objects.all()
    serializer_class = SubCapabilitySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'data': serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'SubCapability created successfully'})
        return Response({'message': 'Something went wrong'})


class IssueViewSet(viewsets.ModelViewSet):
    pass
