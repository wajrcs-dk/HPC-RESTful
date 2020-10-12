RESTful API Server Set Up:
--------------------------

To set up our RESTful API server in GWDG data center, we need to set up a GWDG cloud server<br>
first. The server will have public IP as well as DNS and it is based on Ubuntu 18.04 image in our<br>
case.

Docker:
--------------------------

Installing Docker on Ubuntu:
curl -fsSL https://get.docker.com -o get-docker.sh<br>
sh get-docker.sh<br>
docker -v

MySQL Database:
--------------------------

Installing MySQL docker container:
sudo docker run -d -e MYSQL_ROOT_PASSWORD=pass -p 3325:3306 --name mysql_restapi mysql:5.7

Set up Database:
--------------------------

sudo apt install mysql-client-core-5.7<br>
mysql -uroot -ppass -h127.0.0.1 -P3325<br>
---<br>
CREATE DATABASE ‘hpc_api‘;<br>
USE ‘hpc_api‘;<br>
SET NAMES utf8;<br>
SET time_zone = ’+00:00’;<br>
SET foreign_key_checks = 0;<br>
SET sql_mode = ’NO_AUTO_VALUE_ON_ZERO’;<br>
DROP TABLE IF EXISTS ‘job‘;<br>
CREATE TABLE ‘job‘ (<br>
  ‘job_id‘ int(10) NOT NULL AUTO_INCREMENT,<br>
  ‘hpc_job_id‘ int(10) DEFAULT NULL,<br>
  ‘operation‘ varchar(50) NOT NULL,<br>
  ‘user_id‘ int(10) NOT NULL,<br>
  ‘name‘ varchar(250) NOT NULL,<br>
  ‘commands‘ text NOT NULL,<br>
  ‘job_meta_data‘ text,<br>
  ‘created‘ datetime NOT NULL,<br>
  ‘updated‘ datetime NOT NULL,<br>
  ‘result‘ text,<br>
  ‘log‘ text,<br>
  ‘status‘ varchar(50) NOT NULL,<br>
  PRIMARY KEY (‘job_id‘)<br>
) ENGINE=InnoDB DEFAULT CHARSET=latin1;<br>
DROP TABLE IF EXISTS ‘user‘;<br>
CREATE TABLE ‘user‘ (<br>
  ‘user_id‘ int(11) NOT NULL AUTO_INCREMENT,<br>
  ‘username‘ varchar(50) NOT NULL,<br>
  ‘first_name‘ varchar(50) NOT NULL,<br>
  ‘last_name‘ varchar(50) NOT NULL,<br>
  ‘email‘ varchar(50) NOT NULL,<br>
  ‘password‘ varchar(50) NOT NULL,<br>
  PRIMARY KEY (‘user_id‘)<br>
) ENGINE=InnoDB DEFAULT CHARSET=latin1;<br>
commit;<br>
exit;

Set up RESTful Python Server:
--------------------------

apt-get update<br>
apt-get install apt-file<br>
apt-file update<br>
apt-get install vim<br>
apt install python3-pip<br>
pip3 install mysql-connector<br>
cd ~<br>
mkdir repo<br>
mkdir -p /home/nginx-static/static/<br>
cd repo/<br>
git clone https://gitlab.gwdg.de/waqar-hpc-master-thesis/hpc-restful-core<br>
cp API-Static/hpc.py /home/nginx-static/static/<br>
cd API-Server<br>
pip3 install -r requirements.txt<br>
python3 -m swagger_server

Set up Gunicorn<br>
--------------------------

apt-get install gunicorn3<br>
gunicorn3 -w 3 "swagger_server.server:app"

Set up Supervisor<br>
--------------------------<br>
apt install supervisor<br>
touch /etc/supervisor/conf.d/flask_app.conf<br>
[program:flask_app]<br>
directory=/root/repo/API-Server<br>
command=gunicorn3 -w 3 "swagger_server.server:app"<br>
autostart=true<br>
autorestart=true<br>
stopasgroup=true<br>
killasgroup=true<br>
stderr_logfile=/var/log/flask_app/flask_app.err.log<br>
stdout_logfile=/var/log/flask_app/flask_app.out.log<br>
mkdir /var/log/flask_app<br>
touch /var/log/flask_app/flask_app.out.log<br>
touch /var/log/flask_app/flask_app.err.log<br>
service supervisor start

Nginx Web Server<br>
Installing Nginx Docker Container (while exposing port 8081):
--------------------------<br>
sudo docker run --name nginx_restapi -d -p 8081:80 nginx<br>
sudo docker exec -it nginx_restapi bash<br>
cd /etc/nginx/conf.d/<br>
touch flask_app.conf<br>
server {<br>
  listen 80;<br>
  listen [::]:80;<br>
  server_name localhost;<br>
  access_log /home/access.log;<br>
  error_log /home/error.log warn;<br>
  # serve static files<br>
  location /static/ {<br>
    root /home/nginx-static;<br>
    expires 30d;<br>
  }<br>
  location / {<br>
    proxy_pass http://127.0.0.1:8000;<br>
    proxy_set_header Host $host;<br>
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;<br>
  }<br>
}<br>
rm default.conf<br>
nginx -s reload<br>

Setup Cron Job:
--------------------------

Python:
--------------------------

module load python/3.8.2<br>

Cron Job:
--------------------------

To set up Cron Job we need to understand its command line arguments first.<br>
1. <Host> RESTful API server host or IP.<br>
2. <Port> RESTful API server port.<br>
3. <API endpoint> RESTful API fixed endpoint.<br>
4. <Temporary location> A location to store temporary data.<br>
5. <Time to recheck> Time duration in seconds to recheck for a new job.<br>
6. <Run counter> How many times a Cron Job should look for new jobs.<br>
<br>
We can run Cron Job either using CronTab or Supervisord.<br>
<br>
git clone https://gitlab.gwdg.de/waqar-hpc-master-thesis/hpc-restful-core.git<br>
cd API-Client/<br>
python3 cronjob.py 141.5.101.84 8081 Master-Thesis/HPC-RESTful/1.0.0/ /usr/users/walamgi/data/jobs/ 5 10