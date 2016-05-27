"""
.. module:: tests.test_connection
   :synopsis: python-xirsys Connection Tests

.. moduleauthor:: Alexander Kavanaugh (@kavdev)

"""

from unittest.case import TestCase
from unittest.mock import patch

from python_xirsys.connection import Connection, REST_ENDPOINT
from python_xirsys.exceptions import XirSysAPIException
from tests import JSONDict


class TestConnection(TestCase):

    def setUp(self):
        self.connection = Connection(username="username", secret_key="secret")

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": "test_data"}))
    def test_get(self, request_mock):
        result = self.connection.get(path="/")

        request_mock.assert_called_once_with("GET", url=REST_ENDPOINT + "/", data={"ident": "username", "secret": "secret"})

        self.assertEqual("test_data", result)

    @patch("requests.request", return_value=JSONDict({"s": 500, "e": "forced_exception", "d": None}))
    def test_get_exception(self, request_mock):
        with self.assertRaisesRegex(XirSysAPIException, "XirSys endpoint returned an HTTP 500: forced_exception"):
            self.connection.get(path="/")

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": "test_data"}))
    def test_post(self, request_mock):
        result = self.connection.post(path="/", foo="bar")

        request_mock.assert_called_once_with("POST", url=REST_ENDPOINT + "/", data={"ident": "username", "secret": "secret", "foo": "bar"})

        self.assertEqual("test_data", result)

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": "test_data"}))
    def test_post_with_none(self, request_mock):
        result = self.connection.post(path="/", foo="bar", nonetype=None)

        request_mock.assert_called_once_with("POST", url=REST_ENDPOINT + "/", data={"ident": "username", "secret": "secret", "foo": "bar"})

        self.assertEqual("test_data", result)

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": "test_data"}))
    def test_post_coerce(self, request_mock):
        result = self.connection.post(path="/", foo="bar", intcoerce=42)

        request_mock.assert_called_once_with("POST", url=REST_ENDPOINT + "/", data={"ident": "username", "secret": "secret", "foo": "bar", "intcoerce": "42"})

        self.assertEqual("test_data", result)

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": None}))
    def test_delete(self, request_mock):
        result = self.connection.delete(path="/")

        request_mock.assert_called_once_with("DELETE", url=REST_ENDPOINT + "/", data={"ident": "username", "secret": "secret"})

        self.assertEqual(None, result)
