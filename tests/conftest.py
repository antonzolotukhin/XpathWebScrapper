# -*- coding: utf-8 -*-
import os
import re
from urllib.parse import urlparse
import pytest
from xpathwebscrapper.utils import Config


def request_callback_get(request, context):
    """
    Берем содержимое ответов на GET-запросы из файлов,
    расположенных по соответствующему пути.
    Взято с devopshq/tfs.
    """
    context.status_code, response = get_from_file(request.url)
    return response


def get_from_file(uri):
    path = urlparse(uri).path
    response_file = os.path.normpath("tests/resources/{}".format(path))
    response_file = os.path.join(response_file)

    if os.path.exists(response_file):
        code = 200
        response = open(response_file, mode="r", encoding="utf-8-sig").read()
        print(f"mock {response_file} 200")
    else:
        code = 404
        response = '''"404": "Not Found"'''
        print(f"mock {response_file} 404")
    return code, response


@pytest.fixture()
def httpget_mock(requests_mock):
    """
    Подменяем GET-запросы
    """
    for method in ("GET", "POST", "PUT", "PATCH"):
        requests_mock.register_uri(method, re.compile(r"https://.+/.*"), text=request_callback_get)
    yield


@pytest.fixture()
def inittestconfig():
    print("init testconfig")
    c = Config.getInstance()
    print(c)
    c.parse_args(["tests/resources/test.yml", "tests/resources/test.xlsx"])

    yield

    Config.destroyInstance()
    print("destroy testconfig")


@pytest.fixture()
def destroyconfig():
    yield
    Config.destroyInstance()
