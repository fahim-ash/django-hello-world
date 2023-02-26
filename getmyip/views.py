from django.http import HttpResponse
import os


def index(request):
    # set the header
    from_where = ''
    access_allow_origin = os.getenv('ACCESS_ALLOW_ORIGIN', '*')
    response = HttpResponse('', content_type='text/plain')
    response['Access-Control-Allow-Origin'] = access_allow_origin

    # get IP address
    headers = [
        'HTTP_X_FORWARDED_FOR', 'X_FORWARDED_FOR',
        'HTTP_CLIENT_IP',
        'HTTP_X_REAL_IP',
        'HTTP_X_FORWARDED',
        'HTTP_X_CLUSTER_CLIENT_IP',
        'HTTP_FORWARDED_FOR',
        'HTTP_FORWARDED',
        'HTTP_VIA',
        'REMOTE_ADDR',
    ]
    ip_list = []
    for i in headers:
        x_forwarded_for = request.META.get(i)
        ip = x_forwarded_for

        if ip:
            ip_list.append((i, ip))

    if not ip_list:
        response.status_code = 404
        response.content = b'Not found.'
    else:
        response.content = b'\n'.join([f"{i[0]}: {i[1]}".encode('utf-8') for i in ip_list])

    return response
            