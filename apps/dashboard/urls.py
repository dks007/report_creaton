# dashboard/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.dashboard.views import (  MenuViewSet, ProjectViewSet, SubCapabilityViewSet,
                                  CapabilityViewSet, SuccessCreateReportViewSet, SuccessReportViewSet,
                                   ListViewSet, ExpertViewSet)

router = DefaultRouter()
router.register('menu-card-list', MenuViewSet, basename='menu-card-list')
router.register('project-list', ProjectViewSet, basename='project-list')
router.register('capability', CapabilityViewSet, basename='capability')
router.register('sub-capability', SubCapabilityViewSet, basename='sub-capability')
router.register('report', SuccessReportViewSet, basename='report')
router.register('createreport', SuccessCreateReportViewSet, basename='createreport')
router.register('', ListViewSet, basename='issue-list')
router.register('expertlist', ExpertViewSet, basename='expertlist')
# router.register('issue-list', IssueViewSet, basename='issue-list')

urlpatterns = [
    path('', include(router.urls)),
    #path('issue-listing/', get_issue_list),
    #path('issue-details/<str:id>', get_issue_details),
    #path('get-createreport/<str:id>', get_create_report),
    # path('create-report/', get_issue_details),
    # path('menu-card-listing/', MenuViewSet.as_view({'get': 'list'}))
    # Add any additional URL patterns as needed
]

