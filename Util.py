# --coding:utf8--
import MySQLdb
import time


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

class Booking(object):

    """Docstring for Booking. """
    def __init__(self, ID="", Name="", PlateNumber="", Price="", PayStstus="",
                 ProduceTime="", StartTime="", EndTime="", PID=""):
        """TODO: to be defined1. """
        self.ID = ID
        self.Name = Name
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.PlateNumber = PlateNumber
        self.ProduceTime = ProduceTime
        self.Price = Price
        self.PayStstus = PayStstus
        self.PID = PID

    def book(self):
        conn = get_conn()
        cur = conn.cursor()
        try:
            self.ProduceTime = get_timenow()
            # 获取现在时间
            cur.execute("INSERT INTO `order`( `StartTime`, `EndTime`, \
                        `PlateNumber`, `Name`, `ProduceTime`) VALUES \
                        ('%s','%s','%s','%s','%s')" %
                        (self.StartTime, self.EndTime, self.PlateNumber,
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
        sql = "update `order` set `StartTime` = '%s' , `EndTime` = '%s'  \
            where `ID`='%s'" % (self.StartTime, self.EndTime, self.ID)
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
            for row in results:
                book = Booking(ID=row[8],
                               Name=row[0],
                               PlateNumber=row[1],
                               Price=row[2],
                               PayStstus=row[3],
                               ProduceTime=row[4],
                               PID=row[5],
                               StartTime=row[6],
                               EndTime=row[7])
                result = book
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
    def diplay_book(Name):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(("SELECT * FROM `order` WHERE  `Name`='%s'" % (Name)))
        result = cur.fetchall()
        if len(result) == 0:
            return None
        else:
            temp = []
            for row in result:
                book = Booking(ID=row[8],
                               Name=row[0],
                               PlateNumber=row[1],
                               Price=row[2],
                               PayStstus=row[3],
                               ProduceTime=row[4],
                               PID=row[5],
                               StartTime=row[6],
                               EndTime=row[7])
                temp.append(book)
            return temp
