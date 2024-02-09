# yourapp/utils.py

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

from django.conf import settings
import requests


def get_sharepoint_context():
    site_url = settings.SHAREPOINT_SITE_URL
    ctx_auth = AuthenticationContext(url=site_url)
    ctx_auth.acquire_token_for_user(username=settings.SHAREPOINT_USERNAME, password=settings.SHAREPOINT_PASSWORD)
    ctx = ClientContext(site_url, ctx_auth)
    return ctx


def upload_file_to_sharepoint(file_path, destination_folder):
    ctx = get_sharepoint_context()
    with open(file_path, 'rb') as file_content:
        target_folder = ctx.web.get_folder_by_server_relative_url(destination_folder)
        target_file = target_folder.upload_file(file_path, file_content)
        ctx.execute_query()


def download_file_from_sharepoint(file_path, source_folder, file_name):
    ctx = get_sharepoint_context()
    source_file = ctx.web.get_file_by_server_relative_path(f'{source_folder}/{file_name}')
    with open(file_path, 'wb') as file_content:
        source_file.download(file_content)
        ctx.execute_query()
