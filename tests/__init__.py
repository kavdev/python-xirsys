"""
.. module:: tests.
   :synopsis: python-xirsys Tests

.. moduleauthor:: Alexander Kavanaugh (@kavdev)

"""


class JSONDict(dict):

    def json(self):
        return self
