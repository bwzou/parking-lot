# --coding:utf8--
import redis
from pickle import loads
import time
import sys           # main函数传参

# redis 命令会被用到
# rpush 在列表的末尾插入一个元素
# blpop 从列表开头获取一个元素，如果列表是空则阻塞
# lpop 从列表开头获取一个元素，如果列表是空则返回空
# llen 返回列表的长度


def queue_daemon(app, rv_ttl=500):         # rv_ttl是等待时常
    q = RedisQueue(app.config['REDIS_QUEUE_KEY'])               # 提前配置好app
    while 1:                                             # 每一次轮训
        msg = q.get_nowait()
        if msg is not None:
            dict = loads(msg)           # 调用数据库查询程序(下单，修改，取消)
            print dict
        else:                          # flask端用get()或者size()判断
            time.sleep(1)
    return 0


class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db= redis.Redis(**redis_kwargs)
        self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.
        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)  # 返回的是元组tuple
        else:
            item = self.__db.lpop(self.key)             # 返回的是str

        if item:
            if isinstance(item, tuple):     # 判断是否是元组
                item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)


def main():                           # module可以要也可以不要main函数
    queue_daemon(sys.argv[0])
    print 'hello world!'

if __name__ == '__main__':
    main()
