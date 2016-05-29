# 先cd到项目路径下
from Parking import app
import RedisQueue
RedisQueue.queue_daemon(app)
