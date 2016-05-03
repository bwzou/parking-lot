import MySQLdb


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


class Booking(object):

    """Docstring for Booking. """

    def __init__(self, id="", name="", beginTime="", endTime="", carNumber=""):
        """TODO: to be defined1. """
        self.id = id
        self.name = name
        self.beginTime = beginTime
        self.endTime = endTime
        self.carNumber = carNumber

    def book(self):
        pass

    def alter_book(self):
        pass

    def cancel_book(self):
        pass
