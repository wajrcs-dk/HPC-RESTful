# HPC-RESTful

https://dev.to/hmajid2301/implementing-a-simple-rest-api-using-openapi-flask-connexions-28kk

https://github.com/zalando/connexion/commit/518d1dd3d711782aa56eb406b7fb346443d94271

https://phoenixnap.com/kb/how-to-share-data-between-docker-containers

https://stackoverflow.com/questions/50116182/slurm-how-can-i-prevent-jobs-information-to-be-removed

https://medium.com/@darutk/diagrams-of-all-the-openid-connect-flows-6968e3990660
https://medium.com/@darutk/diagrams-and-movies-of-all-the-oauth-2-0-flows-194f3c3ade85
https://openid.net/developers/certified/
https://github.com/OpenIDC/pyoidc
https://realpython.com/token-based-authentication-with-flask/#register-route

https://www.pramp.com


https://searchapparchitecture.techtarget.com/definition/RESTful-API
https://restfulapi.net/
https://swagger.io/resources/articles/documenting-apis-with-swagger/
https://medium.com/swlh/restful-api-documentation-made-easy-with-swagger-and-openapi-6df7f26dcad
https://www.smashingmagazine.com/2018/01/understanding-using-rest-api/
https://www.baeldung.com/swagger-2-documentation-for-spring-rest-api

https://medium.com/wolox/documenting-a-nodejs-rest-api-with-openapi-3-swagger-5deee9f50420
https://scotch.io/tutorials/speed-up-your-restful-api-development-in-node-js-with-swagger

https://auth0.com/blog/kubernetes-tutorial-step-by-step-introduction-to-basic-concepts/

//////////////////////////////////////

https://flowable.com/open-source/docs/bpmn/ch02-GettingStarted/
https://paulhh.wordpress.com/2017/01/31/flowable-6-instant-gratification/

////////////////////////////////////////

nginx:
docker run --name nginx_restapi -d -p 8081:80 nginx

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
  "name": "Zip Archive HPC v1",
  "command": "zip /data/readme-cmd.zip /data/repo/README.md",
  "jobMetaData": {
    "prerequisites": [
      "zip /data/readme-pre.zip /data/repo/README.md"
    ],
    "postrequisites": [
      "zip /data/readme-post.zip /data/repo/README.md"
    ],
    "output": [
      "ls /data/ | grep '.zip'"
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



--- Docker SLurm Cluster

docker-compose up -d
./register_cluster.sh

docker-compose start
docker-compose stop

docker exec -it slurmctld bash

sinfo

cd /data/

sbatch --wrap="uptime"

slurm-2.out



------


root@wajrcs-Inspiron-5547:/media/wajrcs/01D5823629664230/studies/thesis/work/slurm-docker# docker-compose start
Starting mysql     ... done
Starting slurmdbd  ... done
Starting slurmctld ... done
Starting c1        ... done
Starting c2        ... done
root@wajrcs-Inspiron-5547:/media/wajrcs/01D5823629664230/studies/thesis/work/slurm-docker# docker exec -it slurmctld bash
[root@slurmctld /]# sinfo
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST 
normal*      up 5-00:00:00      2   idle c[1-2] 
[root@slurmctld /]# cd /data/
[root@slurmctld data]# sbatch --wrap="uptime"
Submitted batch job 4
[root@slurmctld data]# cat slurm-4.out 
 12:53:15 up 13:02,  0 users,  load average: 1.14, 0.93, 0.67



 Scontrol
 https://ubccr.freshdesk.com/support/solutions/articles/5000686882
 https://ubccr.freshdesk.com/support/solutions/articles/5000686861-how-do-i-check-the-status-of-my-job-s-

gcc -o Bin/HelloWorld Source/HelloWorld.c

-------------------------

Compile Job

http://172.17.0.4/Master-Thesis/HPC-RESTful/1.0.0/job?accessToken=N9TT-9G0A-B7FQ-RANC


curl -X POST -i 'http://172.17.0.4/Master-Thesis/HPC-RESTful/1.0.0/job?accessToken=N9TT-9G0A-B7FQ-RANC' --data '{"name":"Compile Hello World","commands":[{"subJobType":"unarchive","parameters":"/data/input/HelloWorld.zip|/data/jobs/{jobId}/"},{"subJobType":"compile","parameters":"/data/jobs/{jobId}/Makefile"},{"subJobType":"archive","parameters":"/data/output/HelloWorld-Compiled-{jobId}.zip|/data/jobs/{jobId}/"}],"jobMetaData":{"error":"","output":"/data/output/HelloWorld-Compiled-{jobId}.zip"}}'


/usr/users/walamgi/

{
  "name": "Compile v1",
  "commands": [
    {
      "subJobType": "compile",
      "parameters": "/usr/users/walamgi/data/input/HelloWorld/Makefile"
    }
  ],
  "jobMetaData": {
    "error": "",
    "output": ""
  }
}

{
  "name": "Archive v1",
  "commands": [
    {
      "subJobType": "unarchive",
      "parameters": "/usr/users/walamgi/data/input/HelloWorld.zip|/usr/users/walamgi/data/jobs/{jobId}/"
    }, {
      "subJobType": "archive",
      "parameters": "/usr/users/walamgi/data/output/HelloWorld-{jobId}.zip|/usr/users/walamgi/data/jobs/{jobId}/"
    }
  ],
  "jobMetaData": {
    "error": "",
    "output": "/usr/users/walamgi/data/output/HelloWorld-{jobId}.zip"
  }
}


{
  "name": "Compile v1",
  "commands": [
    {
      "subJobType": "unarchive",
      "parameters": "/data/input/HelloWorld.zip|/data/jobs/{jobId}/"
    }, {
      "subJobType": "compile",
      "parameters": "/data/repo/API-Example/HelloWorld/Source/Makefile"
    }, {
      "subJobType": "archive",
      "parameters": "/data/output/{jobId}.zip|/data/jobs/{jobId}/"
    }
  ],
  "jobMetaData": {
    "error": "",
    "output": "/data/output/{jobId}.zip"
  }
}

{
  "name": "Compile v1",
  "commands": [
    {
      "subJobType": "unarchive",
      "parameters": "/data/input/HelloWorld.zip|/data/jobs/{jobId}/"
    }, {
      "subJobType": "hpc",
      "parameters": "/data/input/MyScript.sh"
    }, {
      "subJobType": "archive",
      "parameters": "/data/output/{jobId}.zip|/data/jobs/{jobId}/"
    }
  ],
  "jobMetaData": {
    "error": "",
    "output": "/data/output/{jobId}.zip"
  }
}

{
  "name": "Compile v1",
  "commands": [
    {
      "subJobType": "unarchive",
      "parameters": "/data/input/HelloWorld.zip|/data/jobs/{jobId}/"
    }, {
      "subJobType": "archive",
      "parameters": "/data/output/{jobId}.zip|/data/jobs/{jobId}/"
    }
  ],
  "jobMetaData": {
    "error": "",
    "output": "/data/output/{jobId}.zip"
  }
}

{
  "name": "Compile v1",
  "commands": [
    {
      "subJobType": "unarchive",
      "parameters": "/data/input/HelloWorld.zip|/data/jobs/{jobId}/"
    }, {
      "subJobType": "compile",
      "parameters": "gcc -o /data/jobs/{jobId}/HelloWorld /data/jobs/{jobId}/HelloWorld.c"
    }, {
      "subJobType": "archive",
      "parameters": "/data/output/{jobId}.zip|/data/jobs/{jobId}/"
    }
  ],
  "jobMetaData": {
    "error": "",
    "output": "/data/output/{jobId}.zip"
  }
}


-------------------------

Compile Job

{
  "name": "Compile v1",
  "command": "gcc -o /data/jobs/{jobId}/HelloWorld /data/jobs/{jobId}/HelloWorld.c",
  "jobMetaData": {
    "prerequisites": [{
      "subJobType": "unarchive",
      "parameters": "/data/input/HelloWorld.zip|/data/jobs/{jobId}/"
    }],
    "postrequisites": [{
      "subJobType": "archive",
      "parameters": "/data/output/{jobId}.zip|/data/jobs/{jobId}/"
    }],
    "output": "/data/output/{jobId}.zip"
  },
  "jobType": "hpc"
}

-------------------------

Bash Job

{
  "name": "Bash Sort v1",
  "command": "/data/input/MyScript.sh",
  "jobMetaData": {
    "prerequisites": [],
    "postrequisites": [{
      "subJobType": "archive",
      "parameters": "/data/output/{jobId}.zip|/data/ouput/SortedRandomNumbers.txt"
    }],
    "output": "/data/output/{jobId}.zip"
  },
  "jobType": "hpc"
}

-------------------------

https://www.gwdg.de/server-services/gwdg-cloud-server 

https://info.gwdg.de/docs/doku.php?id=en:services:application_services:high_performance_computing:connect_with_ssh 

wajrcs@wajrcs-Inspiron-5547:~$ nslookup gwdu102.gwdg.de 
Server:   127.0.0.53
Address:  127.0.0.53#53
Non-authoritative answer:
Name: gwdu102.gwdg.de
Address: 134.76.8.102


Archive Job

{
  "name": "Archive v1",
  "command": "zip /data/readme-cmd.zip /data/repo/README.md",
  "jobMetaData": {
    "prerequisites": [
      "zip /data/readme-pre.zip /data/repo/README.md"
    ],
    "postrequisites": [
      "zip /data/readme-post.zip /data/repo/README.md"
    ],
    "output": [
      "ls /data/ | grep '.zip'"
    ]
  },
  "jobType": "hpc"
}


------------------------------------


Server created
The password is shown in the VNC shell until you logged in for the first time. Please keep the password and store it in a safe place.
User: cloudPassword: (VNC)


https://www.linode.com/docs/development/python/flask-and-gunicorn-on-ubuntu/

https://stackoverflow.com/questions/60253813/gunicorn-flask-connexion-swagger-server-time-out-not-responding-to-api-reque

https://stackoverflow.com/questions/60253813/gunicorn-flask-connexion-swagger-server-time-out-not-responding-to-api-reque

pip3 install mysql-connector
sudo apt-get install gunicorn3
gunicorn -w 3 "swagger_server.__main__:main"


134.76.8.101 
134.76.8.0/24 
10.108.96.101 
CIDR notation 


sudo docker run --detach \
  --hostname gitlab \
  --publish 443:443 --publish 80:80 --publish 22:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab \
  --volume /srv/gitlab/logs:/var/log/gitlab \
  --volume /srv/gitlab/data:/var/opt/gitlab \
  --volume slurm-docker_slurm_jobdir:/data \
  gitlab/gitlab-ce:latest


put host name:
172.17.0.2 gitlab


 docker run -d --name gitlab-runner --restart always \
    --hostname gitlab-runner \
     -v /srv/gitlab-runner/config:/etc/gitlab-runner \
     -v /var/run/docker.sock:/var/run/docker.sock \
     -v slurm-docker_slurm_jobdir:/data \
     gitlab/gitlab-runner:latest

put host name:
172.17.0.3 gitlab-runner

This command registers

docker run --rm -it -v /srv/gitlab-runner/config:/etc/gitlab-runner gitlab/gitlab-runner register

Nginx:
172.17.0.4

import mysql.connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from mysql.connector import pooling
try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                                  pool_size=5,
                                                                  pool_reset_session=True,
                                                                  host='localhost',
                                                                  database='python_db',
                                                                  user='pynative',
                                                                  password='pynative@#29')

    print ("Printing connection pool properties ")
    print("Connection Pool Name - ", connection_pool.pool_name)
    print("Connection Pool Size - ", connection_pool.pool_size)

    # Get connection object from a pool
    connection_object = connection_pool.get_connection()


    if connection_object.is_connected():
       db_Info = connection_object.get_server_info()
       print("Connected to MySQL database using connection pool ... MySQL Server version on ",db_Info)

       cursor = connection_object.cursor()
       cursor.execute("select database();")
       record = cursor.fetchone()
       print ("Your connected to - ", record)

except Error as e :
    print ("Error while connecting to MySQL using Connection pool ", e)
finally:
    #closing database connection.
    if(connection_object.is_connected()):
        cursor.close()
        connection_object.close()
        print("MySQL connection is closed")



gitlab:
    container_name: gitlab_hpc
    image: gitlab/gitlab-ce:latest
    restart: always
    hostname: 'localhost'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://localhost:8929'
        # Add any other gitlab.rb configuration here, each on its own line
    ports:
      - '8929:8929'
      - '2224:22'
    volumes:
      - '/srv/gitlab/config:/etc/gitlab'
      - '/srv/gitlab/logs:/var/log/gitlab'
      - '/srv/gitlab/data:/var/opt/gitlab'
      - slurm_jobdir:/data

  gitlab-runner:
    image: gitlab/gitlab-runner:alpine
    restart: unless-stopped
    container_name: gitlab_runner_hpc
    depends_on:
      - gitlab
    volumes:
      - '/srv/gitlab-runner/config:/etc/gitlab-runner'
      - '/var/run/docker.sock:/var/run/docker.sock'
      - slurm_jobdir:/data



##################333333

sudo su
docker stop ebaf78f0c985
service apache2 stop
service sshd stop
docker start caadf82c5fe8
docker start ebaf78f0c985
docker start 767cc028db4c
docker start e01dafdb6e06
docker exec -it 767cc028db4c bash
service supervisor start
docker exec -it ebaf78f0c985 bash
vi /etc/hosts
docker-compose start
docker exec -it slurmctld bash

------------------

docker-compose stop
docker stop ebaf78f0c985
docker stop caadf82c5fe8
docker stop e01dafdb6e06
docker stop 767cc028db4c