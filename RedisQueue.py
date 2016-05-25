# --coding:utf8--
import redis
from pickle import loads
import time
import Manage
import sys           # main函数传参
from globle import gl
sys.path.append("F:\\pycharmproject\\ParkingLotQQ\\build\\lib.win32-2.7")  # 请把该路径改成你项目lib.win32-2.7的路径
from ParkingAlgorithm import insert                                  # pycharm报错，但不影响

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
            if dict.get('type') == 'change':
                """ we should ascertain whether there is a lot available """
                orders, begin, sustain = Manage.all_lot(dict.get('beginTime'), dict.get('endTime'))
                timeprice = Manage.cal_money(dict.get('beginTime'), dict.get('endTime'), 1)
                if len(orders) == 0:
                    reservation = Manage.Reservation(ID=dict.get('id'),
                                                     PID='A101',
                                                     Name=dict.get('name'),
                                                     StartTime=dict.get('beginTime'),
                                                     EndTime=dict.get('endTime'),
                                                     PlateNumber=dict.get('PlateNumber'),
                                                     ProduceTime=dict.get('time'),
                                                     Price=timeprice)  # 根据sustain来计费
                else:
                    mov_dict = insert(orders, gl.Lots_len, begin, sustain)
                    dict_len = len(mov_dict)
                    if dict_len == 0:  # 如果没有可以用返回[],此时可以给予提示
                        continue    # u'Sorry! There is no a Parkinglotavailable now,failed to alter order', 'error')
                    for i in range(dict_len):
                        if i == 0:
                            reservation = Manage.Reservation(ID=dict.get('id'),
                                                             PID=gl.dict1[mov_dict[0].get('to')],
                                                             Name=dict.get('name'),
                                                             StartTime=dict.get('beginTime'),
                                                             EndTime=dict.get('endTime'),
                                                             PlateNumber=dict.get('PlateNumber'),
                                                             ProduceTime=dict.get('time'),
                                                             Price=timeprice)
                        else:
                            Manage.Reservation.update_lot(mov_dict[i].get('to'), mov_dict[i].get('id'))
                reservation.alter_book()
            elif dict.get('type') == 'create':
                """ we should ascertain whether there is a lot available """
                orders, begin, sustain = Manage.all_lot(dict.get('beginTime'), dict.get('endTime'))
                timeprice = Manage.cal_money(dict.get('beginTime'), dict.get('endTime'), 1)
                if len(orders) == 0:
                    reservation = Manage.Reservation(PID='A101',
                                                     Name=dict.get('name'),
                                                     StartTime=dict.get('beginTime'),
                                                     EndTime=dict.get('endTime'),
                                                     PlateNumber=dict.get('PlateNumber'),
                                                     ProduceTime=dict.get('time'),
                                                     Price=timeprice)
                else:
                    mov_dict = insert(orders, 11, begin, sustain)     # 11为车位总数量，需要动态改变
                    dict_len = len(mov_dict)
                    if dict_len == 0:  # 如果没有可以用返回[]
                        continue    # u'Sorry! There is no a Parkinglot available now'
                    for i in range(dict_len):
                        if i == 0:
                            reservation = Manage.Reservation(PID=gl.dict1[mov_dict[0].get('to')],
                                                             Name=dict.get('name'),
                                                             StartTime=dict.get('beginTime'),
                                                             EndTime=dict.get('endTime'),
                                                             PlateNumber=dict.get('PlateNumber'),
                                                             ProduceTime=dict.get('time'),
                                                             Price=timeprice)
                        else:
                            Manage.Reservation.update_lot(mov_dict[i].get('to'), mov_dict[i].get('id'))
                reservation = reservation.reserve()
            elif dict.get('type') == 'cancel':
                ID = dict.get('id')
                Manage.Reservation.cancel_book(ID)   # 取消订单
        else:                          # flask端用get()或者size()判断
            time.sleep(1)
    return 0


class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db= redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

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
