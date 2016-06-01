# --coding:utf8--
"""
test by Nie Wen
"""
import  Parking
import unittest
import tempfile
import Manage
import  os
import  sqlite3
from contextlib import closing

#def main():
 #   db = Util.init_db()
  #  cursor = db.cursor()
  #  cursor.execute("select * from user")
  #  for item in cursor.fetchall():
  #      print "{},{},{}".format(item[0], item[1], item[2])
    # register = Util.register
    # register(db, cursor, "13752030529", "zhangbiao")
    # db.close()

class parking_test_case(unittest.TestCase):

    app = Parking.app.test_client()
    def setup(self):
        self.db_fb, Parking.app.config['DATABASE'] = tempfile.mkstemp()
        Parking.app.config['TESTING'] = True


    def tearDown(self):
        pass

#---------------------------------------------------------------------------------

    def login(self, username, password):
        return self.app.post('/login', data=dict(inputPhoneNumber=username,
                                                 inputPassword=password), follow_redirects=True)

    def register(self, registUsername, registEmail, registPassword):
        return self.app.post('/register', data=dict(registUsername=registUsername, registEmail=registEmail,
                                                    registPassword=registPassword), follow_redirects=True)

    def test_C_rgister_login(self):
        def test_register(self):
            rv = self.register('12345', '6543@123.com', 'asdf')
            rq = self.login('12345', 'asdf')
            assert 'success register & login' in rq.data
#-----------------------------------------------------------------------------------


#------------------------------------------------------------------------------------
    #   module2
    def reserve(self, time, picker, plate):
        return self.app.post('/reserver', data=dict(slider_value=time, picker=picker,
                                                    plate=plate), follow_redirects=True)

    def change(self, id, time, picker, plate):
        return self.app.post('/change/' + id, data=dict(slider_value=time, picker=picker, plate=plate),
                             follow_redirects=True)

    def test_C_reservation_change(self):
        with Parking.app.test_client().session_transaction() as sess:
            sess['username'] = '111'
        rv = self.reserve('from: 20:45 to: 21:45', '05/11/2016', '987654321')

        with self.app.session_transaction() as sess:
            sess['username'] = '111'
        rv = self.change('321', 'from: 00:45 to: 21:45', '10/11/2016', '000')
#---------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------
#                 module3
    def getlotName(self, inputNumber, inputLicenseNumber):
      return self.app.post('/getlotname', data=dict(inputNumber=inputNumber,
                                                  inputLicenseNumber=inputLicenseNumber),
                         follow_redirects=True)


    def test_getlotName(self):
        rv = self.getlotName('111', '654321')
        assert 'find out lot!!!!' in rv.data

#------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------
#                  module4
    def test_mananger(self):
        username='zuodexin'
        password='111'
        rv=Manage.manager_login(username,password)
        print rv
    #---------------------------get someone reservation histort----------------------------
        username="120"
        rv=Manage.Reservation.display_history_book(username)
    #---------------------------someone reservation  now---------------------------
        username='111'
        rv=Manage.Reservation.display_book(username)
    #----------------------------view parkinglot price now---------------------------
        type='1'
        rv=Manage.get_price(type)

    #----------------------------change parkinglot price---------------------------
#        Manage.set_price('581' , '2016-05-03 09:05:00' , '0.8')

    #-----------------------------manage set advertise----------------------
        Manage.set_promotion('you te jia la','discount ')

    #----------------------------manage get advertise----------------------
        Manage.get_promotion()
if __name__ == "__main__":
    unittest.main()