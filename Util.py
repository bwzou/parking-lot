# --coding:utf8--
import datetime
import time
import MySQLdb


def get_conn():
    # return MySQLdb.connect(user="root", passwd="root", db="parkingLot",
    # unix_socket="/opt/lampp/var/mysql/mysql.sock")
    return MySQLdb.connect(host="121.42.43.36", user="root", passwd="root",
                           db="parkinglot", port=3306)


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
