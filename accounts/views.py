"""
    view file
"""

# django import
from django.http import HttpResponse
from django.conf import settings
import requests


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
    if graph_token:
        url = 'https://graph.microsoft.com/v1.0/users/' + request.user.username
        headers = {
            'Authorization': 'Bearer ' + graph_token['access_token'],
            'Content-type': 'application/json'
        }
        response = requests.get(url=url, headers=headers)
        print(response.json())
        json_response = response.json()
        # print(json_response)

    return HttpResponse("Hey, Login Successfully")


