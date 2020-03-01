# -*- coding: utf-8 -*-
import os
import re
from urllib.parse import urlparse
import json
import httpretty
import pytest


def request_callback_get(request, uri, headers):
    """
    Берем содержимое ответов на GET-запросы из файлов,
    расположенных по соответствующему пути.
    Взято с devopshq/tfs.
    """
    code, response = get_from_file(uri)
    return code, headers, response


def get_from_file(uri):
    path = urlparse(uri).path
    response_file = os.path.normpath('tests/resources/{}'.format(path))
    response_file = os.path.join(response_file)

    if os.path.exists(response_file):
        code = 200
        response = open(response_file, mode="r", encoding="utf-8-sig").read()
        print (f'mock {response_file} 200')
    else:
        code = 404
        response = '''"404": "Not Found"'''
        print (f'mock {response_file} 404')
    return code, response


@pytest.fixture(autouse=True)
def httpget_mock():
    """
    Подменяем GET-запросы во всех (autouse=True) тестах
    """
    for method in (httpretty.GET, httpretty.POST,
                   httpretty.PUT, httpretty.PATCH):
        httpretty.register_uri(method, re.compile(r"https://.+/.*"),
                               body=request_callback_get,
                               content_type="text/html")
