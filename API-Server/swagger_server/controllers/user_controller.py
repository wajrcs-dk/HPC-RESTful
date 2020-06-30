import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


def login_user(username, password):  # noqa: E501
    """Logs user into the system

     # noqa: E501

    :param username: The user name for login
    :type username: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: List[User]
    """
    return 'do some magic!'
