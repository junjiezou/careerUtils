virtualenv --no-site-packages venv
export FLASK_APP=index.py
python -m flask run -h 0.0.0.0 -p 80 &

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

drop table voStrange;
drop table voFamiliar;
create table voStrange (AccountId VARCHAR(64), Word VARCHAR(128),Source VARCHAR(64),UpdateDate DATE);
create table voFamiliar (AccountId VARCHAR(64), Word VARCHAR(128),Source VARCHAR(64)) ;
alter table voStrange modify column UpdateDate datetime ;

### 处理到云服务器上的python版本
- 安装Anaconda
wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
bash Anaconda3-2020.11-Linux-x86_64.sh

- 命令
conda list # 查看安装的包
conda create -n venv list of packages
source activate venv    #进入新环境
source deactivate       #退出
conda env remove -n env_name    #删除
conda env list  # 显示环境
conda env export > environment.yaml # 保存环境
conda env create -f environment.yaml    #迁移环境
conda install --name <env_name> <package_name> # 安装
conda remove --name <env_name> <package_name>   # 卸载
conda install <package_name>    # 在当前环境中安装包
conda remove <package_name>
conda search DBUtils
conda install DBUtils=1.9.3

- 其他命令
新建一个tensorflow环境
conda create -n tensorflow python=3.5
conda activate tensorflow
pip install tensorflow-gpu keras # 安装 gpu 版本的 tensorflow 和 keras
安装需要的环境
conda install ipython
conda install jupyter

- conda源为国内源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes

