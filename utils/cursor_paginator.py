from urllib.parse import urlsplit, parse_qs, urlencode, urlunsplit

from rest_framework import response


def cursor_paginate(viewset, request, *args, **kwargs):
    queryset = viewset.filter_queryset(viewset.get_queryset())

    if not queryset:
        return response.Response({
            'first': None,
            'last': None,
            'next': None,
            'count': 0,
            'results': [],
        })

    count = queryset.count()
    if kwargs.get('reversed'):
        min_id = queryset.last().id
        max_id = queryset.first().id
        cursor = request.query_params.get('cursor', max_id + 1)
        queryset = list(queryset.filter(id__lt=cursor)[:15])
    else:
        min_id = queryset.first().id
        max_id = queryset.last().id
        cursor = request.query_params.get('cursor', 0)
        queryset = list(queryset.filter(id__gt=cursor)[:15])

    if not queryset:
        return response.Response({
            'first': min_id,
            'last': max_id,
            'next': None,
            'count': count,
            'results': [],
        })

    data = viewset.get_serializer(queryset, many=True).data

    last_id = data[-1]['id']
    url = request.build_absolute_uri()
    r = urlsplit(url)
    query = r.query
    params = parse_qs(query)
    params['cursor'] = last_id
    r = r._replace(query=urlencode(params, True))
    url = urlunsplit(r)

    return response.Response({
        'first': min_id,
        'last': max_id,
        'next': url,
        'count': count,
        'results': data,
    })
