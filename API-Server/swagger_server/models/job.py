# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.job_metadata import JobMetadata  # noqa: F401,E501
from swagger_server import util


class Job(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, job_id: int=None, hpc_job_id: int=None, operation: str=None, user_id: int=None, name: str=None, command: str=None, job_meta_data: JobMetadata=None, job_type: str=None, created: datetime=None, updated: datetime=None, result: str=None, log: str=None, status: str=None):  # noqa: E501
        """Job - a model defined in Swagger

        :param job_id: The job_id of this Job.  # noqa: E501
        :type job_id: int
        :param hpc_job_id: The hpc_job_id of this Job.  # noqa: E501
        :type hpc_job_id: int
        :param operation: The operation of this Job.  # noqa: E501
        :type operation: str
        :param user_id: The user_id of this Job.  # noqa: E501
        :type user_id: int
        :param name: The name of this Job.  # noqa: E501
        :type name: str
        :param command: The command of this Job.  # noqa: E501
        :type command: str
        :param job_meta_data: The job_meta_data of this Job.  # noqa: E501
        :type job_meta_data: JobMetadata
        :param job_type: The job_type of this Job.  # noqa: E501
        :type job_type: str
        :param created: The created of this Job.  # noqa: E501
        :type created: datetime
        :param updated: The updated of this Job.  # noqa: E501
        :type updated: datetime
        :param result: The result of this Job.  # noqa: E501
        :type result: str
        :param log: The log of this Job.  # noqa: E501
        :type log: str
        :param status: The status of this Job.  # noqa: E501
        :type status: str
        """
        self.swagger_types = {
            'job_id': int,
            'hpc_job_id': int,
            'operation': str,
            'user_id': int,
            'name': str,
            'command': str,
            'job_meta_data': JobMetadata,
            'job_type': str,
            'created': datetime,
            'updated': datetime,
            'result': str,
            'log': str,
            'status': str
        }

        self.attribute_map = {
            'job_id': 'jobId',
            'hpc_job_id': 'hpcJobId',
            'operation': 'operation',
            'user_id': 'userId',
            'name': 'name',
            'command': 'command',
            'job_meta_data': 'jobMetaData',
            'job_type': 'jobType',
            'created': 'created',
            'updated': 'updated',
            'result': 'result',
            'log': 'log',
            'status': 'status'
        }
        self._job_id = job_id
        self._hpc_job_id = hpc_job_id
        self._operation = operation
        self._user_id = user_id
        self._name = name
        self._command = command
        self._job_meta_data = job_meta_data
        self._job_type = job_type
        self._created = created
        self._updated = updated
        self._result = result
        self._log = log
        self._status = status

    @classmethod
    def from_dict(cls, dikt) -> 'Job':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Job of this Job.  # noqa: E501
        :rtype: Job
        """
        return util.deserialize_model(dikt, cls)

    def update_job_status(old_status, new_status):
        ret = False
        
        if old_status==new_status:
            ret = True

        if old_status=='new' and new_status=='cronjob_in_progress':
            ret = True

        if old_status=='cronjob_in_progress' and new_status=='hpc_queued':
            ret = True

        if old_status=='cronjob_in_progress' and new_status=='cronjob_failed':
            ret = True

        if old_status=='hpc_queued' and new_status=='hpc_in_progress':
            ret = True

        if old_status=='hpc_queued' and new_status=='hpc_aborted':
            ret = True

        if old_status=='hpc_in_progress' and new_status=='hpc_failed':
            ret = True

        if old_status=='hpc_in_progress' and new_status=='completed':
            ret = True

        return ret

    def get_job(job_id):
        sql = "SELECT * FROM `job` WHERE job_id=" + str(job_id)
        return Model.select(sql)

    def insert_job(body):
        sql = "INSERT into `job`"
        sql = sql + " (`hpc_job_id`, `operation`, `user_id`, `name`, `command`, `job_meta_data`, `job_type`, `created`, `updated`, `result`, `log`, `status`) VALUES"
        sql = sql + " (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        val = (
            str(body['hpcJobId']),
            str(body['operation']),
            str(body['userId']),
            str(body['name']),
            str(body['command']),
            str(body['jobMetaData']),
            str(body['jobType']),
            str(body['created']),
            str(body['updated']),
            str(body['result']),
            str(body['log']),
            str(body['status'])
        )
        return Model.insert(sql, val)

    def update_job_operation(job_id, operation):
        sql = "UPDATE `job` SET"
        sql = sql + " operation=%s"
        sql = sql + " WHERE job_id=%s;"
        val = (
            str(operation),
            str(job_id)
        )
        return Model.update(sql, val)

    def update_job(job_id, body):
        sql = "UPDATE `job` SET"
        sql = sql + " hpc_job_id=%s, operation=%s, user_id=%s, name=%s, command=%s, job_meta_data=%s,"
        sql = sql + " job_type=%s, created=%s, updated=%s, result=%s, log=%s, status=%s"
        sql = sql + " WHERE job_id=%s;"
        val = (
            str(body['hpcJobId']),
            str(body['operation']),
            str(body['userId']),
            str(body['name']),
            str(body['command']),
            str(body['jobMetaData']),
            str(body['jobType']),
            str(body['created']),
            str(body['updated']),
            str(body['result']),
            str(body['log']),
            str(body['status']),
            str(job_id)
        )
        return Model.update(sql, val)

    def get_jobs_cout(status):
        if status != None:
            length = len(status)
            for i in range(length): 
                status[i] = "'" + status[i] + "'"
            status = ','.join(status)

        sql = "SELECT count(*) as t FROM `job`"
        if status != None:
            sql = sql + " WHERE `status` in (" + status + ");"
        
        return Model.select(sql)

    def get_jobs(job_status, page_number, page_length):
        '''
        if job_status != None:
            length = len(job_status)
            for i in range(length): 
                job_status[i] = "'" + job_status[i] + "'"
            job_status = ','.join(job_status)
        '''
        job_status = ','.join(job_status)
        sql = "SELECT * FROM `job`"
        if job_status != None:
            sql = sql + " WHERE `status` in (" + job_status + ")"
        sql = sql + " ORDER BY `created` DESC LIMIT " + str((page_number-1)*page_length) + ", " + str(page_length)

        return Model.select(sql)

    def delete_job_status(status):
        ret = False
        
        if status=='new' or status=='cronjob_in_progress' or status=='hpc_queued':
            ret = True

        return ret

    def delete_job(job_id):
        sql = "DELETE FROM `job` WHERE job_id=" + str(job_id) + ";"
        val = ()
        return Model.delete(sql, val)

    @property
    def job_id(self) -> int:
        """Gets the job_id of this Job.


        :return: The job_id of this Job.
        :rtype: int
        """
        return self._job_id

    @job_id.setter
    def job_id(self, job_id: int):
        """Sets the job_id of this Job.


        :param job_id: The job_id of this Job.
        :type job_id: int
        """

        self._job_id = job_id

    @property
    def hpc_job_id(self) -> int:
        """Gets the hpc_job_id of this Job.


        :return: The hpc_job_id of this Job.
        :rtype: int
        """
        return self._hpc_job_id

    @hpc_job_id.setter
    def hpc_job_id(self, hpc_job_id: int):
        """Sets the hpc_job_id of this Job.


        :param hpc_job_id: The hpc_job_id of this Job.
        :type hpc_job_id: int
        """

        self._hpc_job_id = hpc_job_id

    @property
    def operation(self) -> str:
        """Gets the operation of this Job.

        Job Operation  # noqa: E501

        :return: The operation of this Job.
        :rtype: str
        """
        return self._operation

    @operation.setter
    def operation(self, operation: str):
        """Sets the operation of this Job.

        Job Operation  # noqa: E501

        :param operation: The operation of this Job.
        :type operation: str
        """
        allowed_values = ["queue", "abort"]  # noqa: E501
        if operation not in allowed_values:
            raise ValueError(
                "Invalid value for `operation` ({0}), must be one of {1}"
                .format(operation, allowed_values)
            )

        self._operation = operation

    @property
    def user_id(self) -> int:
        """Gets the user_id of this Job.

        User Id or GWDG account number  # noqa: E501

        :return: The user_id of this Job.
        :rtype: int
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: int):
        """Sets the user_id of this Job.

        User Id or GWDG account number  # noqa: E501

        :param user_id: The user_id of this Job.
        :type user_id: int
        """
        if user_id is None:
            raise ValueError("Invalid value for `user_id`, must not be `None`")  # noqa: E501

        self._user_id = user_id

    @property
    def name(self) -> str:
        """Gets the name of this Job.


        :return: The name of this Job.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Job.


        :param name: The name of this Job.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def command(self) -> str:
        """Gets the command of this Job.


        :return: The command of this Job.
        :rtype: str
        """
        return self._command

    @command.setter
    def command(self, command: str):
        """Sets the command of this Job.


        :param command: The command of this Job.
        :type command: str
        """
        if command is None:
            raise ValueError("Invalid value for `command`, must not be `None`")  # noqa: E501

        self._command = command

    @property
    def job_meta_data(self) -> JobMetadata:
        """Gets the job_meta_data of this Job.


        :return: The job_meta_data of this Job.
        :rtype: JobMetadata
        """
        return self._job_meta_data

    @job_meta_data.setter
    def job_meta_data(self, job_meta_data: JobMetadata):
        """Sets the job_meta_data of this Job.


        :param job_meta_data: The job_meta_data of this Job.
        :type job_meta_data: JobMetadata
        """

        self._job_meta_data = job_meta_data

    @property
    def job_type(self) -> str:
        """Gets the job_type of this Job.

        Job Type  # noqa: E501

        :return: The job_type of this Job.
        :rtype: str
        """
        return self._job_type

    @job_type.setter
    def job_type(self, job_type: str):
        """Sets the job_type of this Job.

        Job Type  # noqa: E501

        :param job_type: The job_type of this Job.
        :type job_type: str
        """
        allowed_values = ["hpc", "shell"]  # noqa: E501
        if job_type not in allowed_values:
            raise ValueError(
                "Invalid value for `job_type` ({0}), must be one of {1}"
                .format(job_type, allowed_values)
            )

        self._job_type = job_type

    @property
    def created(self) -> datetime:
        """Gets the created of this Job.


        :return: The created of this Job.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created: datetime):
        """Sets the created of this Job.


        :param created: The created of this Job.
        :type created: datetime
        """

        self._created = created

    @property
    def updated(self) -> datetime:
        """Gets the updated of this Job.


        :return: The updated of this Job.
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated: datetime):
        """Sets the updated of this Job.


        :param updated: The updated of this Job.
        :type updated: datetime
        """

        self._updated = updated

    @property
    def result(self) -> str:
        """Gets the result of this Job.


        :return: The result of this Job.
        :rtype: str
        """
        return self._result

    @result.setter
    def result(self, result: str):
        """Sets the result of this Job.


        :param result: The result of this Job.
        :type result: str
        """

        self._result = result

    @property
    def log(self) -> str:
        """Gets the log of this Job.


        :return: The log of this Job.
        :rtype: str
        """
        return self._log

    @log.setter
    def log(self, log: str):
        """Sets the log of this Job.


        :param log: The log of this Job.
        :type log: str
        """

        self._log = log

    @property
    def status(self) -> str:
        """Gets the status of this Job.

        Job Status  # noqa: E501

        :return: The status of this Job.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this Job.

        Job Status  # noqa: E501

        :param status: The status of this Job.
        :type status: str
        """
        allowed_values = ["new", "cronjob_in_progress", "hpc_queued", "hpc_in_progress", "cronjob_failed", "hpc_failed", "hpc_aborted", "completed"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status