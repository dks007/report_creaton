"""
   dashboard views file
"""

# django import
import json
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.decorators import permission_required

# local import
from apps.dashboard.serializers import MenuListSerializer, ProjectSerializer, CapabilitySerializer, \
    SubCapabilitySerializer, SuccessReportSerializer, SuccessReportSerializer1
from ..accounts.permissions import IFSPermission
from ..utility.create_success_report import success_report, convert_json, all_master_list, upload_logo_image
from ..utility.get_create_report import jiradata_create_report
from ..utility.issue_listing import issue_list_data
from ..utility.issue_details import issue_details_data
from apps.dashboard.models.masters import (MenuCardMaster, ProjectMaster, CapabilityMaster, SubCapabilityMaster,
                                           SDMMaster, SdoMaster, CSMMaster)
from apps.dashboard.models.models import SuccessReport


#@permission_required(IFSPermission)
def get_issue_list(request):
    """
    used to fetch all issues
    """
    if request.method == 'GET':
        response, total_record = issue_list_data(request)
        return JsonResponse({'resdata': response, 'total_record': total_record, 'status': status.HTTP_200_OK})
    else:
        return JsonResponse({'error': 'something went wrong', 'status': status.HTTP_400_BAD_REQUEST})


#@permission_required(IFSPermission)
def get_issue_details(request, id):
    """
    Fetches details of a specific issue.

    Parameters:
    - request: The HTTP request object.
    - id: The ID of the issue to fetch.

    Returns:
    - JsonResponse: A JSON response containing issue details or an error message.
    """
    if request.method == 'GET':
        try:
            response = issue_details_data(request, id)
            return JsonResponse({'data': response, 'status': status.HTTP_200_OK})
        except Issue.DoesNotExist:
            return JsonResponse({'error': 'Issue not found', 'status': status.HTTP_404_NOT_FOUND})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})
    else:
        return JsonResponse({'error': 'Method not allowed', 'status': status.HTTP_405_METHOD_NOT_ALLOWED})



# getting first if data already saved in database 2nd get from jira
#@permission_required(IFSPermission)
def get_create_report(request, id):
    """
    used to fetch specific issue
    """
    if request.method == 'GET':
        response = SuccessReport.objects.filter(jira_key=id).first()
        menu_card, product, capsubcap, customer_contact, customer = all_master_list()
        if not response:
            response = jiradata_create_report(id)
            response['menu_card_list'] = menu_card[0]
            response['product_list'] = product[0]
            response['capsubcap_list'] = capsubcap
            response['customer_contact_list'] = customer_contact[0]
            response['customer_list'] = customer[0]

        else:
            response = {
                "issue_key": response.jira_key,
                "menu_card": response.menu_card.menu_card,
                "capability": response.capability.capability_name,
                "product": response.product.product_name,
                "project_name": response.product.product_name,
                "snow_case_no": response.snow_case_no,
                "expert_name": response.expert.expert_name,
                "customer_contact": response.customer_contact.customer_contact,
                "report_status": response.report_status.report_status_name,
                'menu_card_list': json.loads(menu_card),
                'product_list': json.loads(product),
                'capability_list': json.loads(response.capability.capability_name),
                'customer_list': json.loads(customer)
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
    permission_classes = [IFSPermission]

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
    permission_classes = [IFSPermission]

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
    permission_classes = [IFSPermission]

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
    permission_classes = [IFSPermission]

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


# create popup report
class SuccessReportViewSet1(viewsets.GenericViewSet):
    serializer_class = SuccessReportSerializer1
    permission_classes = [IFSPermission]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Upload logo image if provided
            logo_id = None
            if 'logo' in request.FILES:
                logo_id, error_msg = upload_logo_image(request.FILES['logo'])
                if logo_id:
                    # Save success report with logo id
                    processed_data = success_report(serializer.validated_data, logo_id)
                    return Response({'data': convert_json(processed_data[0]), 'status': status.HTTP_201_CREATED})
                else:
                    return Response({'msg': error_msg, 'status': status.HTTP_404_NOT_FOUND})
            else:
                return Response({'msg': "Logo is required !", 'status': status.HTTP_404_NOT_FOUND})
        return Response({'msg': serializer.errors, 'status': status.HTTP_404_NOT_FOUND})
