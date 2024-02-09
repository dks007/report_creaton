"""
URL configuration for success_tool project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from djangosaml2.views import LoginView, LogoutView


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Reporting Automation",
        default_version='v1',
        description="Reporting Automation",
        terms_of_service="https://yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('api/', include('apps.dashboard.urls')),
    #path('sso/login/', LoginView.as_view(), name='saml_login'),
    #path('sso/logout/', LogoutView.as_view(), name='saml_logout'),


    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
    #      name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
    #      name='schema-redoc'),
]
