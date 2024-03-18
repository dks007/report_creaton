from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
import base64
import json

def base64_to_long(data):
    if isinstance(data, str):
        data = data.encode("ascii")
    rem = len(data) % 4
    if rem > 0:
        data += b'=' * (4 - rem)
    return int.from_bytes(base64.urlsafe_b64decode(data), 'big')

def jwk_to_pem(jwk):
    n = base64_to_long(jwk['n'])
    e = base64_to_long(jwk['e'])
    public_numbers = RSAPublicNumbers(e, n)
    public_key = public_numbers.public_key(backend=default_backend())
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem



# Now you can use 'pem_key' for signature verification
