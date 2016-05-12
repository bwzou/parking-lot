# --coding:utf8--
import datetime
import time
import json

import MySQLdb

from globle import gl


def get_conn():
    # return MySQLdb.connect(user="root", passwd="root", db="parkingLot",
    # unix_socket="/opt/lampp/var/mysql/mysql.sock")
    return MySQLdb.connect(host="121.42.43.36", user="root", passwd="root",
                           db="parkinglot", port=3306)


# -------------------------用户注册登录-------------------------------------------------
def user_exist(cur="", name="", password=""):
    if cur != "":
        cur.execute("SELECT * FROM `user` WHERE  `Name`='%s'" % name)
        return len(cur.fetchall())
    else:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM `user` WHERE `Name`='%s' AND PassWord='%s'"
                    % (name, password))
        result = len(cur.fetchall())
        conn.close()
        return result


def user_login(Name, Password):
    if user_exist(name=Name, password=Password) == 0:
        return "fail"
    else:
        return "success"


def user_register(name, email, phonenumber, password):
    conn = get_conn()
    cur = conn.cursor()
    if user_exist(cur, name) == 0:
        try:
            cur.execute("INSERT INTO `user`( `Name`, `Email`, `PhoneNumber`, \
                        `PassWord` ) VALUES ('%s','%s','%s','%s')" %
                        (name, email, phonenumber, password))
            conn.commit()
            conn.close()
            return "success"
        except:
            conn.rollback()
            conn.close()
            return "fail"
    else:
        conn.close()
        return "exist"

# ---------------------------------订单相关------------------------------------------
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
    timenow = get_timenow()
    time = datetime.datetime.strptime(timenow, "%Y-%m-%d %H:%M:%S")
    futuredata = []
    historydate = []
    for result in data:
        if result.EndTime < time:
            historydate.append(result)
        else:
            futuredata.append(result)
    return futuredata, historydate


# --------------------------------------工具类-----------------------------------------
class Booking(object):
    """Docstring for Booking. """
    def __init__(self, ID="", Name="", PlateNumber="", Price="", PayStatus="",
                 ProduceTime="", StartTime="", EndTime="", PID=""):
        """TODO: to be defined1. """
        self.ID = ID
        self.Name = Name
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.PlateNumber = PlateNumber
        self.ProduceTime = ProduceTime
        self.Price = Price
        self.PayStatus = PayStatus
        self.PID = PID

    def book(self):
        conn = get_conn()
        cur = conn.cursor()
        try:
            self.ProduceTime = get_timenow()        # 获取现在时间
            cur.execute("INSERT INTO `order`( `PID`, `StartTime`, `EndTime`, \
                        `PlateNumber`, `Name`, `ProduceTime`, `Price`) VALUES \
                        ('%s','%s','%s','%s','%s','%s','%s')" %
                        (self.PID, self.StartTime, self.EndTime, self.PlateNumber,
                         self.Name, self.ProduceTime, self.Price))
            conn.commit()
            conn.close()
            return "success"
        except:
            conn.rollback()
            conn.close()
            return "fail"

    def alter_book(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "update `order` set `PID`= '%s', `StartTime` = '%s' , `EndTime` = '%s' , `Price` = '%s' \
            where `ID`='%s'" % (self.PID, self.StartTime, self.EndTime, self.Price, self.ID )
        try:
            cur.execute(sql)
            conn.commit()
            result = "success"
        except:
            conn.rollback()
            result = "fail"
        conn.close()
        return result

    @staticmethod
    def query_book(ID):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select * from `order` where `ID`='%s'" % ID
        try:
            cur.execute(sql)
            results = cur.fetchall()
            result = None
            for row in results:
                print row
                result = Booking(ID=row[8],
                                 Name=row[0],
                                 PlateNumber=row[1],
                                 Price=row[2],
                                 PayStatus=row[3],
                                 ProduceTime=row[4],
                                 PID=row[5],
                                 StartTime=row[6],
                                 EndTime=row[7])
            conn.commit()
        except:
            conn.rollback()
            result = None
        conn.close()
        return result

    @staticmethod
    def query_book_by_plate(plate_number):   # 考虑plate_number不唯一的问题
        conn = get_conn()
        cur = conn.cursor()
        sql = "select * from `order` where `PlateNumber`='%s'AND `EndTime`>= '%s' " \
              "ORDER BY `order`.`EndTime` ASC" % (plate_number,get_timenow())
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                print row
                result = Booking(ID=row[8],
                                 Name=row[0],
                                 PlateNumber=row[1],
                                 Price=row[2],
                                 PayStatus=row[3],
                                 ProduceTime=row[4],
                                 PID=row[5],
                                 StartTime=row[6],
                                 EndTime=row[7])
                conn.commit()
                conn.close()
                return result
        except:
            conn.rollback()
            result = None
        conn.close()
        return result

    @staticmethod
    def cancel_book(ID):
        conn = get_conn()
        cur = conn.cursor()
        sql = "delete from `order` where `ID`='%s'" % ID
        try:
            cur.execute(sql)
            conn.commit()
            result = "success"
        except:
            conn.rollback()
            result = "fail"
        conn.close()
        return result

    @staticmethod
    def update_Lot(new,id):
        sql = "UPDATE `order` SET `PID` = '%s' WHERE `order`.`ID` = '%s' " % (gl.dict1[new], id)
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
            conn.close()
            return True
        except:
            conn.rollback()
            conn.close()
            return False

    @staticmethod
    def diplay_book(Name):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(("SELECT * FROM `order` WHERE  `Name`='%s'" % (Name)))
        result = cur.fetchall()
        if len(result) == 0:
            conn.commit()
            conn.close()
            return None
        else:
            temp = []
            for row in result:
                book = Booking(ID=row[8],
                               Name=row[0],
                               PlateNumber=row[1],
                               Price=row[2],
                               PayStatus=row[3],
                               ProduceTime=row[4],
                               PID=row[5],
                               StartTime=row[6],
                               EndTime=row[7])
                temp.append(book)
            conn.commit()
            conn.close()
            return divide_data(temp)

    @staticmethod
    def select_order(start_time):   # 根据时间查询当前订单及往后两天内的所有预定
        conn = get_conn()
        cur = conn.cursor()
        sql = "SELECT * FROM `order` WHERE  `EndTime`>='%s'ORDER BY `order`.`StartTime` ASC" % start_time
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) == 0:
            conn.commit()
            conn.close()
            return None
        else:
            temp = []
            for row in result:
                print row
                book = Booking(ID=row[8],
                               Name=row[0],
                               PlateNumber=row[1],
                               Price=row[2],
                               PayStatus=row[3],
                               ProduceTime=row[4],
                               PID=row[5],
                               StartTime=row[6],
                               EndTime=row[7])
                temp.append(book)
            conn.commit()
            conn.close()
            return temp

    @staticmethod
    def select_order_by_date(date):  # 根据时间查询当天订单及往后两天内的所有预定
        oneday = datetime.timedelta(days=1)   # 加一天
        nextday = date + oneday
        conn = get_conn()
        cur = conn.cursor()
        sql = "SELECT * FROM `order` WHERE  `StartTime`>='%s'AND `EndTime`<='%s'" \
              "ORDER BY `order`.`StartTime` ASC" % (date, nextday)
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) == 0:
            conn.commit()
            conn.close()
            return None
        else:
            temp = []
            for row in result:
                print row
                book = Booking(ID=row[8],
                               Name=row[0],
                               PlateNumber=row[1],
                               Price=row[2],
                               PayStatus=row[3],
                               ProduceTime=row[4],
                               PID=row[5],
                               StartTime=row[6],
                               EndTime=row[7])
                temp.append(book)
            conn.commit()
            conn.close()
            print temp
            return temp


class ParkingLot(object):
    def __init__(self, ID, Status,NowStatus, Price):
        self.ID = ID
        self.NowStatus = NowStatus
        self.Status = Status
        self.Price = Price

    @staticmethod
    def all_Lot():
        sql = "SELECT * FROM `parkingspace` WHERE `Status`= 1 ORDER BY `parkingspace`.`ID` ASC"
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) == 0:
            conn.commit()
            conn.close()
            return None
        else:
            temp = []
            for row in result:
                Lot = ParkingLot(ID=row[0],
                                 Status=row[1],
                                 NowStatus=row[2],
                                 Price=row[3],)
                temp.append(Lot)
            conn.commit()
            conn.close()
            return temp

class Pricedata(object):
    def __init__(self, price, changeTime, type, ID):
        self.price = price
        self.changeTime = changeTime
        self.type = type
        self.ID = ID

    @staticmethod
    def get_price(type):        # return price from database
        sql = "SELECT * FROM `price` WHERE `type`='%s'" % type
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) == 0:
            conn.commit()
            conn.close()
            return "haha there is nothing"
        else:
            price_all = []
            for r in result:
                p_rice = Pricedata(price=r[0],changeTime=r[1],type=r[2],ID=r[3])
                price_all.append(p_rice)
                conn.commit()
                conn.close()
            return price_all

    @staticmethod
    def set_price(price1,price2,price3):
        sql1 = "update `price` set `price`= '%s' where `type`='0'"  % price1
        sql2 = "update `price` set `price`= '%s' where `type`='1'" % price2
        sql3 ="update `price` set `price`= '%s' where `type`='2'" % price3
        conn = get_conn()
        cur = conn.cursor()
        try:
            if price1 is not None:
                cur.execute(sql1)
            if price2 is not None:
                cur.execute(sql2)
            if price3 is not None:
                cur.execute(sql3)
            conn.commit()
            result = "success"
        except:
            conn.rollback()
            result = "fail"
        conn.close()
        return result


    @staticmethod
    def set_lot_status(ID):
        sql = "Update `parkingspace` SET `NowStatus`='occupied' WHERE `ID`='%s'" % ID
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
            conn.close()
            return "success"
        except:
            conn.rollback()
            conn.commit()
            conn.close()
            return "fail"


# ------------------------转换成可以匹配的数据-----------------------------------------
# match ParkingLot
def match_Lot():
    Lots = ParkingLot.all_Lot()
    gl.Lots_len = len(Lots)
    for i in range(gl.Lots_len):
        gl.dict1[i + 1] = Lots[i].ID
    gl.dict2 = {v: k for k, v in gl.dict1.items()}
    return True


def all_lot(beginTime, endTime):
    orders = Booking.select_order(beginTime)
    key = match_Lot()
    order_datas = []
    if orders == None:     # 最新一笔订单
        flag = beginTime
    else:
        if orders[0].StartTime > beginTime:
            flag = beginTime
        else:
            flag = orders[0].StartTime
        for row in orders:
            startime = int(((row.StartTime - flag) / 900).total_seconds()) + 1
            sustaine = int(((row.EndTime - row.StartTime) / 900).total_seconds())
            order_datas.append((row.ID, gl.dict2[row.PID], startime, sustaine))
        print order_datas

    startime = int(((beginTime - flag) / 900).total_seconds()) + 1
    sustaine = int(((endTime - beginTime) / 900).total_seconds())
    return order_datas, startime, sustaine


def oneday_lot(date):
    orders = Booking.select_order_by_date(date)
    order_datas = []
    if orders == None:
        return order_datas
    else:
        for row in orders:
            one_order = {}            # 必须在循环内定义，否则更改无效
            startime = int(((row.StartTime-date) / 900).total_seconds()) + 1
            sustaine = int(((row.EndTime-date) / 900).total_seconds()) + 1
            one_order['pid'] = row.PID
            one_order['from'] = startime
            one_order['to'] = sustaine
            order_datas.append(one_order)
        print order_datas
    return order_datas


def all_lot_status():
    lots = ParkingLot.all_Lot()
    lots_datas = []
    if lots == None:
        return lots_datas
    else:
        for row in lots:
            one_order = {}   # 必须在循环内定义，否则更改无效
            one_order['pid'] = row.ID
            one_order['state'] = row.NowStatus
            lots_datas.append(one_order)
        print lots_datas
    return lots_datas