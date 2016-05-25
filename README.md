# ParkingLot
Parking.py stands for View
Manage.py stands for Controller
db.py is regarded as Model

安装redis：
pip install flask-redis

运行redis:
D:\Redis-x64-3.0.501\redis-server.exe    # 改路径
D:\Redis-x64-3.0.501\redis-cli.exe

运行Daemon：
1、	导入app，如from RedisQueue import app
2、	Import queue_module
3、queue_module.queue_daemon(app)



