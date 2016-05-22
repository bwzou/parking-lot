# --coding:utf8--
from Util import *          # 导入需要的工具
from globle import gl, Temp


# --------------------------------------实体类-----------------------------------------
class Customer(object):
    def __init__(self, phonenumber, password, name, email):
        self.phonenumber = phonenumber
        self.password = password
        self.name = name
        self.email = email

    @staticmethod
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

    @staticmethod
    def user_login(self, Name, Password):
        if self.user_exist(name=Name, password=Password) == 0:
            return "fail"
        else:
            return "success"

    @staticmethod
    def user_register(self, name, email, phonenumber, password):
        conn = get_conn()
        cur = conn.cursor()
        if self.user_exist(cur, name) == 0:
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


class Booking(object):
    """Docstring for Booking. """
    def __init__(self, ID="", Name="", PlateNumber="", Price="", PayStatus="",
                 ProduceTime="", StartTime="", EndTime="", PID="", comeTime="",
                 leaveTime="", overpay="", overpay_state=""):
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
        self.comeTime = comeTime
        self.leaveTime = leaveTime
        self.overpay = overpay
        self.overpay_state = overpay_state

    def book(self):
        conn = get_conn()
        cur = conn.cursor()
        try:
            self.ProduceTime = get_timenow()        # 获取现在时间
            cur.execute("INSERT INTO `order`( `PID`, `StartTime`, `EndTime`, \
                        `PlateNumber`, `Name`, `ProduceTime`, `Price`) VALUES \
                        ('%s','%s','%s','%s','%s','%s','%s')" %
                        (self.PID, self.StartTime, self.EndTime,
                         self.PlateNumber,
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
        sql = "update `order` set `PID`= '%s', `StartTime` = '%s' , \
            `EndTime` = '%s' , `Price` = '%s' where `ID`='%s'" % \
            (self.PID, self.StartTime, self.EndTime, self.Price, self.ID)
        try:
            cur.execute(sql)
            conn.commit()
            result = "success"
        except:
            conn.rollback()
            result = "fail"
        conn.close()
        return result

    def insert_parktime(self):
        time = get_timenow()
        timetime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        if self.comeTime is not None:
            return 3
        elif (self.StartTime - timetime).seconds > Temp.bfsec and \
                timetime < self.StartTime:
            return 0
        elif (timetime - self.StartTime).seconds > Temp.afsec and \
                timetime > self.StartTime:
            return 1
        else:
            conn = get_conn()
            cur = conn.cursor()
            try:
                cur.execute("update `order` set `comeTime`='%s' where \
                            `ID`='%s'" % (time, self.ID))
                conn.commit()
                result = "success"
            except:
                conn.rollback()
                result = "failture"
            conn.close()
            return result

    def insert_leavetime(self):
        time = get_timenow()
        timetime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        if self.comeTime is None:
            return 0
        elif self.leaveTime is not None:
            return 1
        else:
            self.leaveTime = timetime
            return 2
            conn = get_conn()
            cur = conn.cursor()
            try:
                cur.execute("update `order` set `leaveTime`='%s' where \
                            `ID`='%s'" % (time, self.ID))
                conn.commit()
                result = "success"
            except:
                conn.rollback()
                result = "failture"
            conn.close()
            return result

    def pay_charge(self):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("update `order` set `overpay`='%s', \
                        `overpay_state`='%s', `leaveTime`='%s' where `ID`='%s'"
                        % (self.overpay, "1", self.leaveTime, self.ID))
            conn.commit()
            result = "success"
        except:
            conn.rollback()
            result = "failture"
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
                                 EndTime=row[7],
                                 comeTime=row[9],
                                 leaveTime=row[10],
                                 overpay=row[11],
                                 overpay_state=row[12])
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
        sql = "select * from `order` where `PlateNumber`='%s'AND \
            `EndTime`>= '%s' " "ORDER BY `order`.`EndTime` ASC" % \
            (plate_number, get_timenow())
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
    def update_Lot(new, id):
        sql = "UPDATE `order` SET `PID` = '%s' WHERE `order`.`ID` = '%s' " % \
            (gl.dict1[new], id)
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

    def query_ID(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select ID from `order` where `Name`='%s' and `StartTime`='%s' \
            and `ProduceTime`='%s'" % (self.Name, self.StartTime,
                                       self.ProduceTime)
        try:
            cur.execute(sql)
            temp = cur.fetchall()
            print temp
            for m in temp:
                ID = m[0]
        except:
            ID = "failture"

        conn.close()
        return ID

    def query_money(self):
        if self.leaveTime > self.EndTime and \
                (self.leaveTime - self.EndTime).seconds < 15*60:
            self.overpay = 0
        elif self.leaveTime < self.EndTime:
            self.overpay = 0
        else:
            price = Price.get_singleprice(2)
            m = (self.comeTime - self.leaveTime).seconds / (60 * 15)  # .seconds可以直接获取秒
            real_money = price * m
            self.overpay = int(real_money) - int(self.Price)

    @staticmethod
    def diplay_book(Name):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(("SELECT * FROM `order` WHERE  `Name`='%s'" % (Name)))
        result = cur.fetchall()
        if len(result) == 0:
            conn.commit()
            conn.close()
            return None, None
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
                               EndTime=row[7],
                               comeTime=row[9],
                               leaveTime=row[10],
                               overpay=row[11],
                               overpay_state=row[12])
                temp.append(book)
            conn.commit()
            conn.close()
            return divide_data(temp)

    @staticmethod
    def select_order(start_time):   # 根据时间查询当前订单及往后两天内的所有预定
        conn = get_conn()
        cur = conn.cursor()
        sql = "SELECT * FROM `order` WHERE  `EndTime`>='%s'ORDER BY \
            `order`.`StartTime` ASC" % start_time
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
        sql = "SELECT * FROM `order` WHERE  `StartTime`>='%s'AND \
            `EndTime`<='%s'" "ORDER BY `order`.`StartTime` ASC" % \
            (date, nextday)
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
    def __init__(self, ID, Status, NowStatus, Price):
        self.ID = ID
        self.NowStatus = NowStatus
        self.Status = Status
        self.Price = Price

    @staticmethod
    def all_Lot():
        sql = "SELECT * FROM `parkingspace` WHERE `Status`= 1 ORDER BY \
            `parkingspace`.`ID` ASC"
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

    @staticmethod
    def set_price():
        pass

    @staticmethod
    def get_price(ID):        # return price from database
        sql = "SELECT `Price` FROM `parkingspace` WHERE `ID`= '%s'" % ID
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        conn.commit()
        conn.close()
        if len(result) == 0:
            return None
        else:
            for row in result:
                Lot = row[0]
            return Lot

    @staticmethod
    def set_lot_status(ID):
        sql = "Update `parkingspace` SET `NowStatus`='occupied' WHERE \
            `ID`='%s'" % ID
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


class Price(object):
    def __init__(self, price, changeTime, type, ID):
        self.price = price
        self.changeTime = changeTime
        self.type = type
        self.ID = ID

    @staticmethod
    def get_singleprice(number):
        conn = get_conn()
        cur = conn.cursor()
        sql = "select price from `price` where `ID` = '%s'" % (number)
        try:
            cur.execute(sql)
            prices = cur.fetchall()
            for m in prices:
                price = m[0]
        except:
            price = None
        conn.close()
        return price

    @staticmethod
    def get_price(type):  # return price from database
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
                p_rice = Price(price=r[0], changeTime=r[1], type=r[2], ID=r[3])
                price_all.append(p_rice)
                conn.commit()
                conn.close()
            return price_all

    @staticmethod
    def set_price(price1, price2, price3):
        sql1 = "update `price` set `price`= '%s' where `type`='0'" % price1
        sql2 = "update `price` set `price`= '%s' where `type`='1'" % price2
        sql3 = "update `price` set `price`= '%s' where `type`='2'" % price3
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


class Promotion(object):
    def __init__(self, ID, title, context, time):
        self.ID = ID
        self.title = title
        self.context = context
        self.time = time

    @staticmethod
    def get_promotion():
        sql = "SELECT * FROM `promotion` ORDER BY `time`DESC"          # 根据时间最新来显示
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
                p_rice = Promotion(ID=r[0], title=r[1], context=r[2], time=r[3])
                price_all.append(p_rice)
            conn.commit()
            conn.close()

            return price_all      # 只需要获取一条

    @staticmethod
    def delete_promotion(ID):
        conn = get_conn()
        cur = conn.cursor()
        sql = "delete from `promotion` where `ID`='%s'" % ID
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
    def set_promotion(title, context):
        sql = "INSERT INTO`promotion`(`title`,`content`,`time`) VALUES ('%s', '%s', '%s')"  \
              % (title, context, get_timenow())
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
            conn.close()
            return "success"
        except:
            conn.rollback()
            conn.close()
            return "fail"


class Manager(object):
    def __init__(self, manager_name, password, authority, time):
        self.manager_name = manager_name
        self.password = password
        self.authority = authority
        self.time = time

    @staticmethod
    def manage_login(manager_name, password):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM `manager` WHERE `name`='%s' AND password='%s'"
                    % (manager_name, password))
        result = len(cur.fetchall())
        conn.commit()
        conn.close()
        return result
