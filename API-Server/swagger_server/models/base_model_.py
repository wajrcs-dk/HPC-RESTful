import pprint

import six
import typing

from swagger_server import util

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass",
    database="hpc_api",
    port=3325
)

T = typing.TypeVar('T')


class Model(object):
    # swaggerTypes: The key is attribute name and the
    # value is attribute type.
    swagger_types = {}

    # attributeMap: The key is attribute name and the
    # value is json key in definition.
    attribute_map = {}

    @classmethod
    def from_dict(cls: typing.Type[T], dikt) -> T:
        """Returns the dict as a model"""
        return util.deserialize_model(dikt, cls)

    def to_dict(self):
        """Returns the model properties as a dict

        :rtype: dict
        """
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def select(sql):
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        return mycursor.fetchall()

    def insert(sql, val):
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        return mycursor.lastrowid

    def update(sql, val):
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()

    def delete(sql, val):
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()

    def to_str(self):
        """Returns the string representation of the model

        :rtype: str
        """
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other