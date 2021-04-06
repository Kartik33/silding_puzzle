import sys
sys.path.append("../")

import json
from os import environ as env
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from dotenv import load_dotenv, find_dotenv
import constants
## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''

ENV_FILE=find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
ALGORITHMS = env.get(constants.ALGORITHMS)




class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    auth = request.headers.get('Authorization',None)
    if not auth:
        raise AuthError({
            'code':'authorization_header_missing',
            'description':'Authorization header is expected'
            },401)
    parts = auth.split(" ")
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code':'invalid_header',
            'description':'Authorization header must start with "Bearer"'
            },401)
    elif len(parts) == 1:
        raise AuthError({
            'code':'invalid_header',
            'description':'Token not found"'
            },401)
    elif len(parts) != 3:
        raise AuthError({
            'code':'invalid_header',
            'description':'Authorization header must be token Bearer'
            },401)
    access_token = parts[1]
    id_token = parts[2]
    return access_token,id_token 



def check_permissions(permissions, payload):
    payload_permissions = payload.get('permissions',None)
    if not payload_permissions:
        raise AuthError({
            'code':'invalid_header',
            'description':'Permission must be in the token'
            },400)
    for permission in permissions:
        if permission not in payload['permissions']:
            raise AuthError({
                'code':'invalid_header',
                'description':'Permission must be in the token'
                },400)

    return True 


def verify_decode_id_token(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=CLIENT_ID,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 401)




def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 401)




def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            access_token, id_token = get_token_auth_header()
            try:
                access_payload = verify_decode_jwt(access_token)
                id_payload = verify_decode_id_token(id_token)
                
            except:
                raise AuthError({
                            'code': 'invalid_header',
                            'description': 'Unable to find the appropriate key.'
                        }, 401)
            admin = check_permissions(permission, access_payload)
            return f([access_payload,id_payload], *args, **kwargs)

        return wrapper
    return requires_auth_decorator
