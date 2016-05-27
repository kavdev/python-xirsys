"""
.. module:: tests.test_objects
   :synopsis: python-xirsys Object Tests

.. moduleauthor:: Alexander Kavanaugh (@kavdev)

"""

from unittest.case import TestCase
from unittest.mock import patch

from python_xirsys.connection import Connection, REST_ENDPOINT
from python_xirsys.objects import SignalingServer, ICEServer, Domain, Application, Room
from tests import JSONDict


class TestSignalingServer(TestCase):

    def setUp(self):
        self.connection = Connection(username="username", secret_key="secret")

    def test_instatiate(self):
        server = SignalingServer(connection=self.connection, address="address")
        self.assertEqual("address", server.address)

    def test_str(self):
        server = SignalingServer(connection=self.connection, address="address")
        self.assertEqual("address", str(server))

    def test_repr(self):
        server = SignalingServer(connection=self.connection, address="address")
        self.assertEqual("<SignalingServer [address]>", repr(server))

    def test_equality(self):
        server = SignalingServer(connection=self.connection, address="address")
        self.assertNotEqual("not_address", server)

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": {"token": "test_token"}}))
    def test_generate_token(self, request_mock):
        result = SignalingServer.generate_token(connection=self.connection, domain="test", application="test", room="test")
        self.assertEqual("test_token", result)

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": {"value": "server_address"}}))
    def test_list_all(self, request_mock):
        result = SignalingServer.list_all(connection=self.connection)
        self.assertEqual("server_address", result)


class TestIceServer(TestCase):

    def setUp(self):
        self.connection = Connection(username="username", secret_key="secret")

    def test_instatiate(self):
        server = ICEServer(connection=self.connection, url="url", server_type="stun")
        self.assertEqual("url", server.url)
        self.assertEqual("stun", server.server_type)

    def test_str(self):
        server = ICEServer(connection=self.connection, url="url", server_type="stun")
        self.assertEqual("url", str(server))

    def test_repr(self):
        server = ICEServer(connection=self.connection, url="url", server_type="stun")
        self.assertEqual("<ICEServer [url]>", repr(server))

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": {"iceServers": [{"url": "server_address"}]}}))
    def test_list_all(self, request_mock):
        result = ICEServer.list_all(connection=self.connection, domain="test", application="test", room="test")
        self.assertEqual(["server_address"], result)


class TestDomain(TestCase):

    def setUp(self):
        self.connection = Connection(username="username", secret_key="secret")

    def test_instatiate(self):
        domain = Domain(connection=self.connection, name="name")
        self.assertEqual("name", domain.name)

    def test_str(self):
        domain = Domain(connection=self.connection, name="name")
        self.assertEqual("name", str(domain))

    def test_repr(self):
        domain = Domain(connection=self.connection, name="name")
        self.assertEqual("<Domain [name]>", repr(domain))

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": ["domain.com", "test.com"]}))
    def test_list_all(self, request_mock):
        result = Domain.list_all(connection=self.connection)
        self.assertEqual(["domain.com", "test.com"], result)

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": "created"}))
    def test_create(self, request_mock):
        result = Domain.create(connection=self.connection, domain="test")
        self.assertEqual("test", result)

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": "deleted"}))
    def test_delete(self, request_mock):
        domain = Domain(connection=self.connection, name="name")
        domain.delete()

        request_mock.assert_called_once_with("DELETE", url=REST_ENDPOINT + "/domain", data={"ident": "username", "secret": "secret", "domain": "name"})

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": ["test"]}))
    def test_applications(self, request_mock):
        domain = Domain(connection=self.connection, name="name")
        applications = domain.applications

        self.assertEqual(["test"], applications)

        request_mock.assert_called_once_with("GET", url=REST_ENDPOINT + "/application", data={"ident": "username", "secret": "secret", "domain": "name"})


class TestApplication(TestCase):

    def setUp(self):
        self.connection = Connection(username="username", secret_key="secret")

    def test_instatiate(self):
        application = Application(connection=self.connection, name="name", domain="test.com")
        self.assertEqual("name", application.name)

    def test_str(self):
        application = Application(connection=self.connection, name="name", domain="test.com")
        self.assertEqual("name", str(application))

    def test_repr(self):
        application = Application(connection=self.connection, name="name", domain="test.com")
        self.assertEqual("<Application [name]>", repr(application))

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": ["test1", "test2"]}))
    def test_list_all(self, request_mock):
        result = Application.list_all(connection=self.connection, domain="domain.com")
        self.assertEqual(["test1", "test2"], result)

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": "created"}))
    def test_create(self, request_mock):
        result = Application.create(connection=self.connection, domain="domain.com", application="test")
        self.assertEqual("test", result)

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": "deleted"}))
    def test_delete(self, request_mock):
        application = Application(connection=self.connection, name="name", domain="domain.com")
        application.delete()

        request_mock.assert_called_once_with("DELETE", url=REST_ENDPOINT + "/application", data={"ident": "username", "secret": "secret", "domain": "domain.com", "application": "name"})

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": ["test_room"]}))
    def test_rooms(self, request_mock):
        application = Application(connection=self.connection, name="name", domain="domain.com")
        rooms = application.rooms

        self.assertEqual(["test_room"], rooms)

        request_mock.assert_called_once_with("GET", url=REST_ENDPOINT + "/room", data={"ident": "username", "secret": "secret", "domain": "domain.com", "application": "name"})


class TestRoom(TestCase):

    def setUp(self):
        self.connection = Connection(username="username", secret_key="secret")

    def test_instatiate(self):
        room = Room(connection=self.connection, name="name", domain="test.com", application="test")
        self.assertEqual("name", room.name)

    def test_str(self):
        room = Room(connection=self.connection, name="name", domain="test.com", application="test")
        self.assertEqual("name", str(room))

    def test_repr(self):
        room = Room(connection=self.connection, name="name", domain="test.com", application="test")
        self.assertEqual("<Room [name]>", repr(room))

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": ["test_room1", "test_room2"]}))
    def test_list_all(self, request_mock):
        result = Room.list_all(connection=self.connection, domain="domain.com", application="test")
        self.assertEqual(["test_room1", "test_room2"], result)

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": "created"}))
    def test_create(self, request_mock):
        result = Room.create(connection=self.connection, domain="domain.com", application="test", room="test_room")
        self.assertEqual("test_room", result)

    @patch("requests.request", return_value=JSONDict({"s": 200, "e": None, "d": "deleted"}))
    def test_delete(self, request_mock):
        room = Room(connection=self.connection, name="name", domain="domain.com", application="test")
        room.delete()

        request_mock.assert_called_once_with("DELETE", url=REST_ENDPOINT + "/room", data={"ident": "username", "secret": "secret", "domain": "domain.com", "application": "test", "room": "name"})
