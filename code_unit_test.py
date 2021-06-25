#!/usr/bin/env python3
# Called by running:
# pytest code_unit_test.py
import sys
import pytest
from code_test import CodeTest


def test_python_version():
    pyversion = sys.version_info
    assert pyversion.major == 3 and pyversion.minor == 8

def test_requests_installed():
    result = False
    try:
        import requests
        result = True
    except:
        pass
    assert result == True


def test_wrong_non_int():
    test_obj = CodeTest()
    exception = False
    try:
        test_obj.get_post_by_id("foo")
    except TypeError:
        exception = True
    assert exception


@pytest.mark.xfail()
def test_wrong_non_int():
    test_obj = CodeTest()
    test_obj.get_post_by_id("foo")


@pytest.mark.xfail()
def test_wrong_post_data():
    test_obj = CodeTest()
    test_obj.create_post(userid="foo")


def test_response_code():
    test_obj = CodeTest()
    response = test_obj.get_post_by_id(1)
    assert response.ok


def test_post_create():
    test_obj = CodeTest()
    response = test_obj.create_post(
        title="test",
        userid=1000,
        body="test body"
    )
    assert response.ok


def test_post_delete():
    test_obj = CodeTest()
    response = test_obj.delete_post(
        post_id=10
    )
    assert response.ok


@pytest.mark.xfail()
def test_get_post_by_id_out_of_range():
    test_obj = CodeTest()
    test_obj.get_post_by_id(post_id=0)
