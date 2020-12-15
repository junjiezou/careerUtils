virtualenv --no-site-packages venv
export FLASK_APP=index.py
python -m flask run

## mariadb
### 安装
yum install mariadb
yum install mariadb-server
### 启动
systemctl start mariadb  #启动MariaDB
systemctl stop mariadb  #停止MariaDB
systemctl restart mariadb  #重启MariaDB
systemctl enable mariadb  #设置开机启动

### 命令
mysqladmin --version
mysqladmin -u root password "v@2018ocA";
create database vocabulary;
CREATE USER 'vocabulary'@'%' IDENTIFIED BY 'v@2018ocA';
GRANT ALL PRIVILEGES ON vocabulary.* TO 'vocabulary'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

create table voStrange (AccountId VARCHAR(64), Word VARCHAR(128),Source VARCHAR(64),UpdateDate DATE);
create table voFamiliar (AccountId VARCHAR(64), Word VARCHAR(128),Source VARCHAR(64)) ;