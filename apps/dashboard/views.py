"""
   dashboard views file
"""

# django import
import json
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.decorators import permission_required

# local import
from apps.dashboard.serializers import MenuListSerializer, ProjectSerializer, CapabilitySerializer, \
    SubCapabilitySerializer, SuccessReportSerializer, SuccessCreateReportSerializer
from ..accounts.permissions import IFSPermission
from ..utility.create_success_report import success_report, convert_json, all_master_list, upload_logo_image
from ..utility.get_create_report import jiradata_create_report
from ..utility.issue_listing import issue_list_data
from ..utility.issue_details import issue_details_data
from apps.dashboard.models.masters import (MenuCardMaster, ProjectMaster, CapabilityMaster, SubCapabilityMaster,
                                           SDMMaster, SdoMaster, CSMMaster)
from apps.dashboard.models.models import SuccessReport


class ListViewSet(viewsets.GenericViewSet):

    permission_classes = [IFSPermission]

    @action(methods=['get'], detail=False, url_path='issue-list', url_name='issue-list')
    def issue_list(self, request):
        response, total_record = issue_list_data(request)
        return Response({'resdata': response, 'total_record': total_record, 'status': status.HTTP_200_OK})

    @action(methods=['get'], detail=True, url_path='issue-details', url_name='issue-details')
    def issue_details(self, request, *args, **kwargs):
        response = issue_details_data(request, kwargs['pk'])
        return Response({'resdata': response, 'status': status.HTTP_200_OK})

    @action(methods=['get'], detail=True, url_path='get-create-report', url_name='get-create-report')
    def get_create_report(self, request, *args, **kwargs):
        try:
            report = SuccessReport.objects.filter(jira_key=kwargs['pk']).first()
            menu_card, product, capsubcap, customer_contact, customer = all_master_list()
            if not report:
                # Creating a new report
                report_data = jiradata_create_report(request, kwargs['pk'])
                report_data['menu_card_list'] = menu_card[0]
                report_data['product_list'] = product[0]
                report_data['capsubcap_list'] = capsubcap
                report_data['customer_contact_list'] = customer_contact[0]
                report_data['customer_list'] = customer[0]
            else:
                report_data = {
                    "issue_key": report.jira_key,
                    "menu_card": report.menu_card.menu_card if report.menu_card else "",
                    "sdo_name": report.sdo.sdo_name if report.sdo else "",
                    "csm_name": report.csm.csm_name if report.csm else "",
                    "sdm_name": report.sdm.sdm_name if report.sdm else "",
                    "capability": report.capability.capability_name if report.capability else "",
                    "sub_capability": report.sub_capability.sub_capability_name if report.sub_capability else "",
                    "product": report.product.product_name if report.product else "",
                    "customer_name": report.customer.customer_name if report.customer else "",
                    "snow_case_no": report.snow_case_no,
                    "expert_name": report.expert.expert_name if report.expert else "",
                    "customer_contact": report.customer_contact.customer_contact if report.customer_contact else "",
                    "report_status": report.report_status.report_status_name if report.report_status else "",
                    'menu_card_list': menu_card[0],
                    'product_list': product[0],
                    'capsubcap_list': capsubcap,
                    'customer_list': customer[0],
                    'customer_contact_list': customer_contact[0],
                    'logo_file_name': report.logo.logo_file_name if report.logo else "",
                    'logo_url': report.logo.logo_url if report.logo else ""
                }
            return JsonResponse({'resdata': report_data, 'status': status.HTTP_200_OK})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

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
            return JsonResponse({'resdata': response, 'status': status.HTTP_200_OK})
        except id.DoesNotExist:
            return JsonResponse({'error': 'Issue not found', 'status': status.HTTP_404_NOT_FOUND})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})
    else:
        return JsonResponse({'error': 'Method not allowed', 'status': status.HTTP_405_METHOD_NOT_ALLOWED})



# getting first if data already saved in database 2nd get from jira
#@permission_required(IFSPermission)
def get_create_report(request, id):
    """
    Fetches an existing report or creates a new one if not found.
    
    Parameters:
        request (HttpRequest): The request object.
        jira_key (str): The Jira key for the report.
        
    Returns:
        JsonResponse: A JSON response with the report data or an error message.
    """
    if request.method == 'GET':
        try:
            # Checking if report already exists in the table
            report = SuccessReport.objects.filter(jira_key=id).first()
            menu_card, product, capsubcap, customer_contact, customer = all_master_list()
            if not report:
                # Creating a new report
                report_data = jiradata_create_report(request, id)
                report_data['menu_card_list'] = menu_card[0]
                report_data['product_list'] = product[0]
                report_data['capsubcap_list'] = capsubcap
                report_data['customer_contact_list'] = customer_contact[0]
                report_data['customer_list'] = customer[0]
            else:
                report_data = {
                    "issue_key": report.jira_key,
                    "menu_card": report.menu_card.menu_card if report.menu_card else "",
                    "sdo_name": report.sdo.sdo_name if report.sdo else "",
                    "csm_name": report.csm.csm_name if report.csm else "",
                    "sdm_name": report.sdm.sdm_name if report.sdm else "",
                    "capability": report.capability.capability_name if report.capability else "",
                    "sub_capability": report.sub_capability.sub_capability_name if report.sub_capability else "",
                    "product": report.product.product_name if report.product else "",
                    "customer_name": report.customer.customer_name if report.customer else "",
                    "snow_case_no": report.snow_case_no,
                    "expert_name": report.expert.expert_name if report.expert else "",
                    "customer_contact": report.customer_contact.customer_contact if report.customer_contact else "",
                    "report_status": report.report_status.report_status_name if report.report_status else "",
                    'menu_card_list': menu_card[0],
                    'product_list': product[0],
                    'capsubcap_list': capsubcap,
                    'customer_list': customer[0],
                    'customer_contact_list': customer_contact[0],
                    'logo_file_name': report.logo.logo_file_name if report.logo else "",
                    'logo_url': report.logo.logo_url if report.logo else ""
                }
            return JsonResponse({'resdata': report_data, 'status': status.HTTP_200_OK})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})
    else:
        return JsonResponse({'error': 'Method not allowed', 'status': status.HTTP_405_METHOD_NOT_ALLOWED})

class MenuViewSet(viewsets.ModelViewSet):
    """
    menu card view set, used to get menu list and specific record
    """
    queryset = MenuCardMaster.objects.all()
    serializer_class = MenuListSerializer
    #permission_classes = [IFSPermission]

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
    #permission_classes = [IFSPermission]

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
    #permission_classes = [IFSPermission]

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
    #permission_classes = [IFSPermission]

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
    #permission_classes = [IFSPermission]

    def create(self, request, *args, **kwargs):
        """
        create report
        """
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'success-report created successfully!', 'status': status.HTTP_201_CREATED})
        return Response({'msg': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST})
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
class SuccessCreateReportViewSet(viewsets.GenericViewSet):
    serializer_class = SuccessCreateReportSerializer
    #permission_classes = [IFSPermission]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Upload logo image if provided
            logo_id = None
            if 'logo' in request.FILES:
                logo_id, error_msg = upload_logo_image(request.FILES['logo'],request.data.get('customer_name', ''))
                if logo_id:
                    # Save success report with logo id
                    msg = success_report(serializer.validated_data, logo_id)
                    return Response({'msg': msg, 'status': status.HTTP_201_CREATED})
                else:
                    return Response({'msg': error_msg, 'status': status.HTTP_404_NOT_FOUND})
            else:
                return Response({'msg': "Logo is required !", 'status': status.HTTP_404_NOT_FOUND})
        return Response({'msg': serializer.errors, 'status': status.HTTP_404_NOT_FOUND})
