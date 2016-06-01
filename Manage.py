# --coding:utf8--
"""
coding by Zou Bowen, Zhang Biao,Feng Fan
"""
from db import *


# ------------------------转换成可以匹配的数据-----------------------------------------
def match_Lot():
    Lots = ParkingLot.all_Lot()
    gl.Lots_len = len(Lots)
    for i in range(gl.Lots_len):
        gl.dict1[i + 1] = Lots[i].ID
    gl.dict2 = {v: k for k, v in gl.dict1.items()}
    return True


def all_lot(beginTime, endTime):
    orders = Booking.select_order(beginTime)
    match_Lot()
    order_datas = []
    if orders is None:     # 最新一笔订单
        flag = beginTime
    else:
        if orders[0].StartTime > beginTime:
            flag = beginTime
        else:
            flag = orders[0].StartTime
        for row in orders:
            startime = int(((row.StartTime - flag) / 900).total_seconds()) + 1
            sustaine = \
                int(((row.EndTime - row.StartTime) / 900).total_seconds())
            order_datas.append((row.ID, gl.dict2[row.PID], startime, sustaine))

    startime = int(((beginTime - flag) / 900).total_seconds()) + 1
    sustaine = int(((endTime - beginTime) / 900).total_seconds())
    return order_datas, startime, sustaine


def oneday_order_lot(date):
    orders = Booking.select_order_by_date(date)
    order_datas = []
    if orders is None:
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
    return order_datas


def all_lot_status():
    lots = ParkingLot.all_Lot()
    lots_datas = []
    if lots is None:
        return lots_datas
    else:
        for row in lots:
            one_order = {}   # 必须在循环内定义，否则更改无效
            one_order['pid'] = row.ID
            one_order['state'] = row.NowStatus
            lots_datas.append(one_order)
    return lots_datas


def set_lot_status(PID):
    ans = ParkingLot.set_lot_status(PID)
    return ans


def set_lot_status_idle(PID):
    ans = ParkingLot.set_lot_status_idle(PID)
    return ans


# -----------------------用户注册登录------------------------------------------------
def user_register(name, email, phonenumber, password):
    result = Customer.user_register(Customer, name, email, phonenumber, password)   # Customer代表self
    return result


def user_login(phone, password):
    result = Customer.user_login(Customer, phone, password)
    return result


# ----------------------经理登陆----------------------------------------------------
def manager_login(name, password):
    result = Manager.manage_login(name, password)
    if result == 0:
        return "fail"
    else:
        return "success"


# ---------------------价格与信息-----------------------------------------------------
def get_price(type):
    result = Price.get_price(type)
    return result


def set_price(price, overstay, discounts):
    result = Price.set_price(price, overstay, discounts)
    return result


def cal_money(startTime, endTime, number):
    m = (endTime - startTime).seconds/(60 * 15)
    price = Price.get_singleprice(number)
    return m*price


def get_promotion():
    result = Promotion.get_promotion()
    return result


def get_single_promotion(ID):
    result = Promotion.get_single_promotion(ID)
    return result


def set_promotion(title, context):
    result = Promotion.set_promotion(title, context)
    return result


def delete_promotion(ID):
    result = Promotion.delete_promotion(ID)
    return result


# -------------------订单相关-------------------------------------------------------
class Reservation(object):
    """Docstring for Booking. """
    def __init__(self, ID="", Name="", PlateNumber="", Price="", PayStatus="",
                 ProduceTime="", StartTime="", EndTime="", PID="", comeTime="",
                 leaveTime="", overpay="", overpay_state="", diff=""):
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
        self.diff = diff

    def reserve(self):
        book = Booking(PID=self.PID,
                       Name=self.Name,
                       StartTime=self.StartTime,
                       EndTime=self.EndTime,
                       PlateNumber=self.PlateNumber,
                       ProduceTime=self.ProduceTime,
                       Price=self.Price)
        result = book.book()
        return result, book.ProduceTime


    def alter_book(self):
        book = Booking(ID=self.ID,
                       PID=self.PID,
                       Name=self.Name,
                       StartTime=self.StartTime,
                       EndTime=self.EndTime,
                       PlateNumber=self.PlateNumber,
                       ProduceTime=self.ProduceTime,
                       Price=self.Price)
        result = book.alter_book()
        return result

    @staticmethod
    def diplay_book(name):
        data, history = Booking.diplay_book(name)
        return data, history

    @staticmethod
    def diplay_history_book(name):
        history = Booking.diplay_history_book(name)
        return history

    @staticmethod
    def update_lot(to, id):
        result = Booking.update_Lot(to, id)
        return result

    @staticmethod
    def query_book(ID):
        result = Booking.query_book(ID)
        return result

    def query_ID(self):
        book = Booking(ID=self.ID,
                       PID=self.PID,
                       Name=self.Name,
                       StartTime=self.StartTime,
                       EndTime=self.EndTime,
                       PlateNumber=self.PlateNumber,
                       ProduceTime=self.ProduceTime,
                       Price=self.Price)

        result = book.query_ID()
        # result = book.alter_book()
        return result

    def pay_debt(self):
        book = Booking(ID=self.ID,
                       PID=self.PID,
                       Name=self.Name,
                       StartTime=self.StartTime,
                       EndTime=self.EndTime,
                       PlateNumber=self.PlateNumber,
                       ProduceTime=self.ProduceTime,
                       Price=self.Price,
                       diff=self.diff)
        result = book.pay_debt()
        return result

    @staticmethod
    def cancel_book(ID):
        result = Booking.cancel_book(ID)
        return result

    @staticmethod
    def query_book_by_plate(plate_number):
        ans = Booking.query_book_by_plate(plate_number)
        return ans

    @staticmethod
    def query_by_name_produceTime(dt, name):
        ans = Booking.query_by_name_produceTime(dt, name)
        return ans

    @staticmethod
    def query_book(ID):
        result = Booking.query_book(ID)
        return result
