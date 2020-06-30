# HPC-RESTful

https://dev.to/hmajid2301/implementing-a-simple-rest-api-using-openapi-flask-connexions-28kk

https://github.com/zalando/connexion/commit/518d1dd3d711782aa56eb406b7fb346443d94271

////////////////////////////////////////

mysql:
docker run --rm -d -e MYSQL_ROOT_PASSWORD=pass -p 3325:3306 --name mysql_test mysql:5.7
mysql -uroot -ppass -h127.0.0.1 -P3325

pass is password

////////////////////////////////////////

pip3 install mysql-connector-python

////////////////////////////////////////

Insert:
http://0.0.0.0:8080/Master-Thesis/HPC-RESTful/1.0.0/job?name=Test&command=uptime&jobMetaData={}&jobType=hpc&accessToken=N9TT-9G0A-B7FQ-RANC

http://0.0.0.0:8080/Master-Thesis/HPC-RESTful/1.0.0/job?name=Test&command=uptime&jobMetaData=%7B%0A%20%20%22prerequisites%22%3A%20%5B%0A%20%20%20%20%22ls%20-lh%22%0A%20%20%5D%2C%0A%20%20%22postrequisites%22%3A%20%5B%0A%20%20%20%20%22ls%20-lh%22%0A%20%20%5D%2C%0A%20%20%22output%22%3A%20%5B%0A%20%20%20%20%22output.txt%22%0A%20%20%5D%0A%7D&jobType=hpc&accessToken=N9TT-9G0A-B7FQ-RANC

List:
http://0.0.0.0:8080/Master-Thesis/HPC-RESTful/1.0.0/job/findJobsByStatus?status=cronjob_in_progress&pageLength=10&pageNumber=1&accessToken=N9TT-9G0A-B7FQ-RANC

Get 1:
http://0.0.0.0:8080/Master-Thesis/HPC-RESTful/1.0.0/job/1?accessToken=N9TT-9G0A-B7FQ-RANC

Update everything 1:
http://0.0.0.0:8080/Master-Thesis/HPC-RESTful/1.0.0/job/1?accessToken=N9TT-9G0A-B7FQ-RANC

Update 2:
http://0.0.0.0:8080/Master-Thesis/HPC-RESTful/1.0.0/job/updateByOperation/1?operation=abort&accessToken=N9TT-9G0A-B7FQ-RANC

////////////////////////////////////////

Insert:

curl -X POST -H 'accept: application/json' -H 'Content-Type: application/json' -i 'http://0.0.0.0:8080/Master-Thesis/HPC-RESTful/1.0.0/job?name=Test&command=uptime&jobMetaData={}&jobType=hpc&accessToken=N9TT-9G0A-B7FQ-RANC'

List:

curl -X GET -H 'accept: application/json' -H 'Content-Type: application/json' -i 'http://0.0.0.0:8080/Master-Thesis/HPC-RESTful/1.0.0/job/findJobsByStatus?status=new&pageLength=10&pageNumber=1&accessToken=N9TT-9G0A-B7FQ-RANC'

Get 1:

curl -X GET -H 'accept: application/json' -H 'Content-Type: application/json' -i 'http://0.0.0.0:8080/Master-Thesis/HPC-RESTful/1.0.0/job/1?accessToken=N9TT-9G0A-B7FQ-RANC'

Update everything 1:

curl -X PUT -H 'accept: application/json' -H 'Content-Type: application/json' -i 'http://0.0.0.0:8080/Master-Thesis/HPC-RESTful/1.0.0/job/1?accessToken=N9TT-9G0A-B7FQ-RANC' --data '{
  "command": "string",
  "created": "2020-06-23 11:11:11",
  "hpcJobId": 0,
  "jobId": 1,
  "jobMetaData": {
    "output": [
      "string"
    ],
    "postrequisites": [
      "string"
    ],
    "prerequisites": [
      "string"
    ]
  },
  "jobType": "hpc",
  "log": "string",
  "name": "string",
  "operation": "abort",
  "result": "string",
  "status": "new",
  "updated": "2020-06-23 11:11:11",
  "userId": 0
}'

Update 2:

curl -X PUT -H 'accept: application/json' -H 'Content-Type: application/json' -i 'http://0.0.0.0:8080/Master-Thesis/HPC-RESTful/1.0.0/job/updateByOperation/1?operation=abort&accessToken=N9TT-9G0A-B7FQ-RANC'


Meeting-ID: 988 8024 9168
Passwort: 940979

My: 867826

+ code didnt work
+ Yaml changes
+ Authentication didn't work
+ Added a new edit api
+ Added token
+ connexion
+ bug fixing in connexion
+ mysql / docker setup
+ issue with post body / + problem with post params


{
  "name": "string",
  "command": "string",
  "jobMetaData": {
    "prerequisites": [
      "string"
    ],
    "postrequisites": [
      "string"
    ],
    "output": [
      "string"
    ]
  },
  "jobType": "hpc"
}



create database `hpc_api`;


-- Adminer 4.7.7 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `job`;
CREATE TABLE `job` (
  `job_id` int(10) NOT NULL AUTO_INCREMENT,
  `hpc_job_id` int(10) DEFAULT NULL,
  `operation` varchar(50) NOT NULL,
  `user_id` int(10) NOT NULL,
  `name` varchar(250) NOT NULL,
  `command` text NOT NULL,
  `job_meta_data` text,
  `job_type` varchar(50) NOT NULL,
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `result` text,
  `log` text,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- 2020-06-27 19:49:20

https://github.com/tuupola/pybranca

new
cronjob_in_progress
hpc_queued
hpc_in_progress
completed
hpc_failed
cronjob_failed
hpc_aborted
