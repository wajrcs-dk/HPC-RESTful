Install Docker on Ubuntu

$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sh get-docker.sh

$ docker -v

-----------------------------------------------------

Install NginX Docker

sudo docker run --name nginx_restapi -d -p 8081:80 nginx

-----------------------------------------------------

----
Install Vim
apt-get update
apt-get install apt-file
apt-file update
apt-get install vim
----

Setup NginX

sudo docker exec -it nginx_restapi bash
cd /etc/nginx/conf.d/
touch flask_app.conf
rm default.conf
nginx -s reload
apt-get install gunicorn3
apt install python3-pip
pip3 install mysql-connector

-----------------------------------------------------

Setup Repository

cd ~
mkdir repo
cd repo/
git init
git pull origin master




-----------------------------------------------------

Install Mysql Docker

sudo docker run -d -e MYSQL_ROOT_PASSWORD=pass -p 3325:3306 --name mysql_restapi mysql:5.7
sudo apt install mysql-client-core-5.7
mysql -uroot -ppass -h127.0.0.1 -P3325

-----------------------------------------------------

Setup MySQL Database

CREATE DATABASE `hpc_api`;
USE `hpc_api`;

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
  `commands` text NOT NULL,
  `job_meta_data` text,
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

commit;


exit;