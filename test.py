import Util


def main():
    db = Util.init_db()
    cursor = db.cursor()
    cursor.execute("select * from user")
    for item in cursor.fetchall():
        print "{},{},{}".format(item[0], item[1], item[2])
    # register = Util.register
    # register(db, cursor, "13752030529", "zhangbiao")
    # db.close()

if __name__ == "__main__":
    main()
