# ParkingLot
Parking.py stands for View
Manage.py stands for Controller
db.py is regarded as Model

部署网站前需要做以下几步：
1、安装redis：
pip install flask-redis

2、运行run.bat:
需要把run.bat里面的redis-server.exe改成项目下install_redis路径


3、python run.by   # cmd 里先cd到单前路径下
目的：
1、	导入app，如from RedisQueue import app
2、	Import queue_module
3、queue_module.queue_daemon(app)



