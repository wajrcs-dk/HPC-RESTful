# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.job import Job  # noqa: E501
from swagger_server.models.job_metadata import JobMetadata  # noqa: E501
from swagger_server.test import BaseTestCase


class TestJobController(BaseTestCase):
    """JobController integration test stubs"""

    def test_add_job(self):
        """Test case for add_job

        Schedules a new job to the HPC system
        """
        query_string = [('access_token', 'access_token_example')]
        response = self.client.open(
            '/Master-Thesis/HPC-RESTful/1.0.0/job'.format(name='name_example', command='command_example', job_meta_data=JobMetadata(), job_type='job_type_example'),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_job(self):
        """Test case for delete_job

        Deletes an existing job
        """
        query_string = [('access_token', 'access_token_example')]
        response = self.client.open(
            '/Master-Thesis/HPC-RESTful/1.0.0/job/{jobId}'.format(job_id=789),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_find_jobs_by_status(self):
        """Test case for find_jobs_by_status

        Finds jobs, optionally by status
        """
        query_string = [('status', 'status_example'),
                        ('page_length', 789),
                        ('page_number', 789),
                        ('access_token', 'access_token_example')]
        response = self.client.open(
            '/Master-Thesis/HPC-RESTful/1.0.0/job/findJobsByStatus',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_job_by_id(self):
        """Test case for get_job_by_id

        Finds job by ID
        """
        query_string = [('access_token', 'access_token_example')]
        response = self.client.open(
            '/Master-Thesis/HPC-RESTful/1.0.0/job/{jobId}'.format(job_id=789),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_job(self):
        """Test case for update_job

        Updates an existing job
        """
        body = Job()
        query_string = [('access_token', 'access_token_example')]
        response = self.client.open(
            '/Master-Thesis/HPC-RESTful/1.0.0/job/{jobId}'.format(job_id=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_job_by_operation(self):
        """Test case for update_job_by_operation

        Updates operation of an existing job
        """
        query_string = [('access_token', 'access_token_example')]
        response = self.client.open(
            '/Master-Thesis/HPC-RESTful/1.0.0/job/updateByOperation/{jobId}'.format(job_id=789, operation='operation_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
