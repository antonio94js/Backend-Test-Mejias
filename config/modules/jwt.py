from datetime import timedelta

config = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'myprivatekey',
    'USER_ID_CLAIM': 'id',
}