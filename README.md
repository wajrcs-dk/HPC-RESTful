RESTful API Server Set Up:
--------------------------

To set up our RESTful API server in GWDG data center, we need to set up a GWDG cloud server
first. The server will have public IP as well as DNS and it is based on Ubuntu 18.04 image in our
case.

Docker:
--------------------------

Installing Docker on Ubuntu:
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
docker -v

MySQL Database:
--------------------------

Installing MySQL docker container:
sudo docker run -d -e MYSQL_ROOT_PASSWORD=pass -p 3325:3306 --name mysql_restapi mysql
:5.7

Set up Database:
--------------------------

sudo apt install mysql-client-core-5.7
mysql -uroot -ppass -h127.0.0.1 -P3325
---
CREATE DATABASE ‘hpc_api‘;
USE ‘hpc_api‘;
SET NAMES utf8;
SET time_zone = ’+00:00’;
SET foreign_key_checks = 0;
SET sql_mode = ’NO_AUTO_VALUE_ON_ZERO’;
DROP TABLE IF EXISTS ‘job‘;
CREATE TABLE ‘job‘ (
  ‘job_id‘ int(10) NOT NULL AUTO_INCREMENT,
  ‘hpc_job_id‘ int(10) DEFAULT NULL,
  ‘operation‘ varchar(50) NOT NULL,
  ‘user_id‘ int(10) NOT NULL,
  ‘name‘ varchar(250) NOT NULL,
  ‘commands‘ text NOT NULL,
  ‘job_meta_data‘ text,
  ‘created‘ datetime NOT NULL,
  ‘updated‘ datetime NOT NULL,
  ‘result‘ text,
  ‘log‘ text,
  ‘status‘ varchar(50) NOT NULL,
  PRIMARY KEY (‘job_id‘)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS ‘user‘;
CREATE TABLE ‘user‘ (
  ‘user_id‘ int(11) NOT NULL AUTO_INCREMENT,
  ‘username‘ varchar(50) NOT NULL,
  ‘first_name‘ varchar(50) NOT NULL,
  ‘last_name‘ varchar(50) NOT NULL,
  ‘email‘ varchar(50) NOT NULL,
  ‘password‘ varchar(50) NOT NULL,
  PRIMARY KEY (‘user_id‘)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
commit;
exit;

Set up RESTful Python Server:
--------------------------

apt-get update
apt-get install apt-file
apt-file update
apt-get install vim
apt install python3-pip
pip3 install mysql-connector
cd ~
mkdir repo
mkdir -p /home/nginx-static/static/
cd repo/
git clone https://gitlab.gwdg.de/waqar-hpc-master-thesis/hpc-restful-core
cp API-Static/hpc.py /home/nginx-static/static/
cd API-Server
pip3 install -r requirements.txt
python3 -m swagger_server

Set up Gunicorn
--------------------------

apt-get install gunicorn3
gunicorn3 -w 3 "swagger_server.server:app"

Set up Supervisor
--------------------------
apt install supervisor
touch /etc/supervisor/conf.d/flask_app.conf
[program:flask_app]
directory=/root/repo/API-Server
command=gunicorn3 -w 3 "swagger_server.server:app"
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/flask_app/flask_app.err.log
stdout_logfile=/var/log/flask_app/flask_app.out.log
mkdir /var/log/flask_app
touch /var/log/flask_app/flask_app.out.log
touch /var/log/flask_app/flask_app.err.log
service supervisor start

Nginx Web Server
Installing Nginx Docker Container (while exposing port 8081):
--------------------------
sudo docker run --name nginx_restapi -d -p 8081:80 nginx
sudo docker exec -it nginx_restapi bash
cd /etc/nginx/conf.d/
touch flask_app.conf
server {
  listen 80;
  listen [::]:80;
  server_name localhost;
  access_log /home/access.log;
  error_log /home/error.log warn;
  # serve static files
  location /static/ {
    root /home/nginx-static;
    expires 30d;
  }
  location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
}
rm default.conf
nginx -s reload

Setup Cron Job:
--------------------------

Python:
--------------------------

module load python/3.8.2


Cron Job:
--------------------------

To set up Cron Job we need to understand its command line arguments first.
1. <Host> RESTful API server host or IP.
2. <Port> RESTful API server port.
3. <API endpoint> RESTful API fixed endpoint.
4. <Temporary location> A location to store temporary data.
5. <Time to recheck> Time duration in seconds to recheck for a new job.
6. <Run counter> How many times a Cron Job should look for new jobs.

We can run Cron Job either using CronTab or Supervisord.

git clone https://gitlab.gwdg.de/waqar-hpc-master-thesis/hpc-restful-core.git
cd API-Client/
python3 cronjob.py 141.5.101.84 8081 Master-Thesis/HPC-RESTful/1.0.0/ /usr/users/walamgi
/data/jobs/ 5 10