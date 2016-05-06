# --coding:utf8--
import gl
import MySQLdb
import time
import datetime



def get_conn():
    # return MySQLdb.connect(user="root", passwd="root", db="parkingLot",
    # unix_socket="/opt/lampp/var/mysql/mysql.sock")
    return MySQLdb.connect(host="121.42.43.36", user="root", passwd="root",
                           db="parkinglot", port=3306)


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
            self.ProduceTime = get_timenow()             # 获取现在时间
            cur.execute("INSERT INTO `order`( `PID`, `StartTime`, `EndTime`, \
                        `PlateNumber`, `Name`, `ProduceTime`) VALUES \
                        ('%s','%s','%s','%s','%s','%s')" %
                        (self.PID, self.StartTime, self.EndTime, self.PlateNumber,
                         self.Name, self.ProduceTime))
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
        sql = "update `order` set `PID`= '%s', `StartTime` = '%s' , `EndTime` = '%s'  \
            where `ID`='%s'" % (self.PID, self.StartTime, self.EndTime, self.ID)
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
    def query_book_by_plate(plate_number):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select * from `order` where `PlateNumber`='%s'" % plate_number
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


class ParkingLot(object):
    def __init__(self, ID, Status, Price):
        self.ID = ID
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
                                 Price=row[2])
                temp.append(Lot)
            conn.commit()
            conn.close()
            return temp


# match ParkingLot
def match_Lot():
    Lots = ParkingLot.all_Lot()
    gl.Lots_len = len(Lots)
    for i in range(gl.Lots_len):
        gl.dict1[i+1] = Lots[i].ID
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
            sustaine = int(((row.EndTime - row.StartTime) / 900).total_seconds()) + 1
            order_datas.append((row.ID, gl.dict2[row.PID], startime, sustaine))
        print order_datas

    startime = int(((beginTime - flag) / 900).total_seconds()) + 1
    sustaine = int(((endTime - beginTime) / 900).total_seconds()) + 1
    return order_datas, startime, sustaine

