# from Parking import insert
# param1:[(reservation_id,parkinglot_id,start,time_len)]
# param2:num_parking_lot  where all of the 1<=parking_lot_id<=num_parking_lot
# param3:start time of new reservation
# param4:length of the new reservation.Notice endtime=start time+ length -1
# return [] when too crowed to insert
# return [(rid,-1,pid),(rid,from,to),...] when success.
import sys
sys.path.append("./build/lib.win32-2.7")
from Parking import insert
print insert([(1,1,1,3),(2,1,6,3),(3,2,2,5),(4,3,1,4),(5,3,7,2)],3,4,3)


# import Util
#
#
# def main():
#     db = Util.init_db()
#     cursor = db.cursor()
#     cursor.execute("select * from user")
#     for item in cursor.fetchall():
#         print "{},{},{}".format(item[0], item[1], item[2])
#     # register = Util.register
#     # register(db, cursor, "13752030529", "zhangbiao")
#     # db.close()
#
# if __name__ == "__main__":
#     main()
