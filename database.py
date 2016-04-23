import MySQLdb

def get_conn():
    host="127.0.0.1"
    port=3306
    user="root"
    passwords="123"
    db="parkinglot"
    conn=MySQLdb.connect(host=host,
                         user=user,
                         passwd=passwords,
                         db=db,
                         port=port,
                         charset="utf8")
    return  conn

def user_login(email,password):
    conn=get_conn()
    cur=conn.cursor()
    sql="SELECT * FROM `user` WHERE `Email`='%s' AND PassWord='%s' " % (email, password)
    cur.execute(sql)
    result=cur.fetchall()
    if len(result)== 0:
        conn.close()
        return  "fail"
    else:
        conn.close()
        return  "success"

def user_register(name,email,phonenumber,password):
    conn=get_conn()
    cur=conn.cursor()
    sql1 = "SELECT * FROM `user` WHERE  `Name`='%s' AND `Email`='%s' AND `PhoneNumber`='%s'AND `PassWord`='%s'" % (
    name, email, phonenumber, password)
    cur.execute(sql1)
    result = cur.fetchall()
    if len(result)==0:
        sql = "INSERT INTO `user`( `Name`, `Email`, `PhoneNumber`, `PassWord`) VALUES ('%s','%s','%s','%s')" % (
        name, email, phonenumber, password)
        cur.execute(sql)

        conn.commit()

        cur.execute(sql1)
        result=cur.fetchall()
        if len(result)==1:
            conn.close()
            return "success"
        if len(result)==0:
            conn.close()
            return  "fail"
    else:
        conn.close()
        return  "exist"