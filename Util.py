# --coding:utf8--
import datetime
import time
import MySQLdb


def get_conn():
    return MySQLdb.connect(host="121.42.43.36", user="root", passwd="root",
                           db="parkinglot", port=3306, charset='utf8')


def get_timenow():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def change_time(result):
    return time.mktime(result.timetuple())*1000


def change_timetostr(result):
    return result.strftime("%m/%d/%Y")


def change_bookto(result):
    result.ProduceTime = change_timetostr(result.StartTime)
    result.StartTime = change_time(result.StartTime)
    result.EndTime = change_time(result.EndTime)
    return result


def divide_data(data):
    futuredata = []
    historydate = []
    for result in data:
        # if result.EndTime < time:
        if result.comeTime is not None:
            historydate.append(result)
        else:
            futuredata.append(result)
    return futuredata, historydate

def get_today():
    return datetime.datetime.today()


def get_ex_day(day, number):
    return day + datetime.timedelta(days=number)


def get_ex_day_list():
    list = []
    for i in range(-6, 1, 1):
        list.append(get_ex_day(get_today(), i))
    return list


def get_day_form(day):
    return day.strftime("%d-%b-%y")


def get_days_form():
    list = []
    for i in get_ex_day_list:
        list.append(get_day_form(i))
    return list


def get_day_zero(day):
    return datetime.datetime(day.year, day.month, day.day, 0, 0)


def select_db(sql):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
    except:
        result = "fail"
    conn.close()
    return result


class salary(object):
    def __init__(self, date="", profit=0, reservation=0, daytime=""):
        self.date = date
        self.profit = profit
        self.reservation = reservation

    def get_all_today_money(self):
        date = get_day_zero(self.date)
        sql = "select * from `history` where `ProduceTime`<'%s' and \
            `ProduceTime`>'%s' and `PayStatus`='%s'" % \
            (get_ex_day(date, 1), date, 1)
        result = select_db(sql)
        self.reservation = len(result)
        if result == "fail":
            return None
        else:
            for each in result:
                self.profit += get_single_money(each)
        self.date = get_day_form(self.date)


def get_single_money(m):
    money = 0;
    if m is None:
        return money
    if m[3] == '1':
        money += m[2]
    elif m[12] == 1:
        money += m[11]
    else:
        pass
    return money


def convert_to_dict(obj):
    dict = {}
    dict.update(obj.__dict__)
    return dict


def convert_to_dicts(objs):
    obj_arr = []

    for o in objs:
        dict = {}
        dict.update(o.__dict__)
        obj_arr.append(dict)

    return obj_arr


def class_to_dict(obj):

    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__

    if is_list or is_set:
        return convert_to_dicts(obj)
    else:
        return convert_to_dict(obj)