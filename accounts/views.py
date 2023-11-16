"""
    view file
"""

# django import
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from django.conf import settings
import requests
from rest_framework.response import Response

from accounts.serializers import UserSerializer


def get_graph_token():
    url = settings.AD_URL
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(url=url, headers=headers, data=data)
    return response.json()


def ms_login(request):
    graph_token = get_graph_token()
    print(request.user, ">>>>>>>>>>>>")
    if graph_token:
        url = 'https://graph.microsoft.com/v1.0/users/' + request.user.username
        print(url)
        headers = {
            'Authorization': 'Bearer ' + graph_token['access_token'],
            'Content-type': 'application/json'
        }
        response = requests.get(url=url, headers=headers)
        print(response.json())
        json_response = response.json()
        # print(json_response)

    return HttpResponse("Hey, Login Successfully")


class JiraItem(viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.filter(id=self.kwargs['pk']).first()

    def get_queryset(self):
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response({"User": serializer.data})

