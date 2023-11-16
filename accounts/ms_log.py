# AD_URL = "https://login.microsoftonline.com/{}/auth2/v2.0/token?"
# LOGIN_URL='django_ath_adfs:login'
# LOGIN_REDIRECT = '/'
#
# TENANT_ID = 'f8cdef31-a31e-4b4a-93e4-5f571e91255a'
# CLIENT_ID = '84adf757-2d5a-4c56-8cc1-3e57367a2102'
# CLIENT_SECRET = 'MyO8Q~D1Rd01LcqDC6G.7.C3pveqdB9isJDwFdwV'
#
# AUTH_ADFS = {
#     'AUDIENCE': CLIENT_ID,
#     'CLIENT_ID': CLIENT_ID,
#     'CLIENT_SECRET': CLIENT_SECRET,
#     'CLAIM_MAPPING': {
#         'first_name': 'given_name',
#         'last_name': 'family_name',
#         'email': 'upn'
#     },
#     'GROUPS_CLAIM': 'roles',
#     'MIRROR_GROUPS': True,
#     'USERNAME_CLAIM': 'upn',
#     'TENANT_ID': TENANT_ID,
#     'RELYING_PARTY_ID': CLIENT_ID,
#
# }


url = "https://login.microsoftonline.com/5c9b264f-33ad-4093-bb65-8d14aaec9f63/discovery/v2.0/keys"
valid_audience = 'api://0d44e6da-8e5b-4e98-94b5-5f02ce228647'

response = urlopen(url)
jwks = json.loads(response.read())


def is_logged_in(func):
    def wrapper(self, *args, **kwargs):
        token = self.headers['Authorization'][7:]  # Need to test this against the frontend request.
        try:
            jwks_client = PyJWKClient(url)
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            decoded = jwt.decode(token,
                             signing_key.key,
                             algorithms=["RS256"],
                             audience=valid_audience)

            return func(self, *args, **kwargs)
        except Exception as e:
            print(e)
            return HttpResponse('Unauthorized', status=401)

    wrapper.__name__ = func.__name__
    return wrapper
