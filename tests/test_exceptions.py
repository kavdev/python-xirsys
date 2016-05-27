"""
.. module:: tests.test_exceptions
   :synopsis: python-xirsys Exception Tests

.. moduleauthor:: Alexander Kavanaugh (@kavdev)

"""

from unittest.case import TestCase

from python_xirsys.exceptions import XirSysAPIException


class TestExceptions(TestCase):

    def test_xirsys_api_exception(self):
        """ Yes, this is silly."""

        with self.assertRaises(XirSysAPIException):
            raise XirSysAPIException()
