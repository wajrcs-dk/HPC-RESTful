import pprint

import six
import typing

from swagger_server import util

import mysql.connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from mysql.connector import pooling

T = typing.TypeVar('T')

class Model(object):
    # swaggerTypes: The key is attribute name and the
    # value is attribute type.
    swagger_types = {}

    # attributeMap: The key is attribute name and the
    # value is json key in definition.
    attribute_map = {}

    mydb = {}

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

    def connect(self):
        ret = ''
        try:
            connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="pynative_pool",
                pool_size=5,
                pool_reset_session=True,
                host='172.17.0.1',
                database='hpc_api',
                user='root',
                password='pass',
                port=3325
            )
            # Get connection object from a pool
            self.mydb = connection_pool.get_connection()
        except Error as e:
            ret = "Error while connecting to MySQL using Connection pool " + str(e)
        return ret

    def close(self):
        # closing database connection.
        if(self.mydb.is_connected()):
            self.mydb.close()

    def select(self, sql):
        mycursor = self.mydb.cursor()
        mycursor.execute(sql)
        return mycursor.fetchall()

    def insert(self, sql, val):
        mycursor = self.mydb.cursor()
        mycursor.execute(sql, val)
        self.mydb.commit()
        return mycursor.lastrowid

    def update(self, sql, val):
        mycursor = self.mydb.cursor()
        mycursor.execute(sql, val)
        self.mydb.commit()

    def delete(self, sql, val):
        mycursor = self.mydb.cursor()
        mycursor.execute(sql, val)
        self.mydb.commit()

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
