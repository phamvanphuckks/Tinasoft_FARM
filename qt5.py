from PyQt5           import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QInputDialog, QAction, QGroupBox, QTableWidget, QTableWidgetItem, QWidget, QMessageBox
from PyQt5.QtCore    import QTimer, QTime, QThread, pyqtSignal, Qt, QObject
from PyQt5.QtGui     import QPixmap, QCloseEvent, QColor

import constant  as CONSTANT
import sys, socket, logging
from datetime import datetime

logging.basicConfig(filename='logs\\error_code.log',level=logging.DEBUG)

class qt5Class(QtCore.QObject):
    # The arguments to pyqtSignal define the types of objects that will be emit'd on that signal
    my_signal = pyqtSignal(int)


    def __init__(self):
        try:
            QtCore.QObject.__init__(self)
            self.App = QtWidgets.QApplication([])
            self.app = uic.loadUi("guis\\main.ui")
            self.app.closeEvent = self.closeEvent # khi close, gọi sự kiện closeEvent
            self.app.label_12.hide()
            self.LCD_Number()
            self.initialize()

            # self.Update_RF_Relay()
        except:
            logging.debug('qt5, __init__ : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))            

    def get_password(self):
        try: 
            """Return Google account password."""
            password, ok = QtWidgets.QInputDialog.getText(
                self.parent(), "Password", "Password:",
                QtWidgets.QLineEdit.Password
            )
            return password if ok else ''
        except:
            logging.debug('qt5, get_password : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def backup_Synchronous(self, value):
        try:
            self.my_signal.connect(self.backup_Synchronous_Slot)
            self.my_signal.emit(value)
        except:
            logging.debug('qt5, backup_Synchronous : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    @QtCore.pyqtSlot(int)
    def backup_Synchronous_Slot(self, value):
        try:
            if(value == 0):
                self.app.label_12.show()
                self.app.label_12.setPixmap(QtGui.QPixmap("icons\\backup.png"))

                self.app.label_2.show()
                self.app.label_2.setText("Backup dữ liệu")   
                self.app.label_2.setStyleSheet("QLabel {color:rgb(255, 0, 0)}")  
            elif(value == 1):
                self.app.label_12.show()
                self.app.label_12.setPixmap(QtGui.QPixmap("icons\\sync.png"))
                self.app.label_2.show()
                self.app.label_2.setText("Đang đồng bộ")
                self.app.label_2.setStyleSheet("QLabel {color:rgb(0, 170, 0)}") 
            elif(value == 2):
                self.app.label_2.hide()
                self.app.label_12.hide()  
            else:
                self.app.label_2.hide()
                self.app.label_12.hide()   
        except:
            logging.debug('qt5, backup_Synchronous_Slot : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))             

    def debugg(self, error, information):
        try:
            QMessageBox.critical(self.app, error, information)
        except:
            logging.debug('qt5, debugg : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))    

    def initialize(self): # khi mình khởi động off hết
        try: 
            for i in range(1, 6):
                self.UpdatePicture(i, 0)
            if(self.check_internet()== True):
                self.display_internet(1)
            else:
                self.display_internet(0)
            self.app.label_2.hide()
            self.app.btn_auto.setStyleSheet("QPushButton {background-color: rgb(229, 229, 229);}")
        except:
            logging.debug('qt5, initialize : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))    


    def closeEvent(self, event: QCloseEvent):
        try:
            reply = QMessageBox.critical(self.app, 'Window Close', 'Are you sure you want to close the window?',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
                # print('Window closed')
            else:
                event.ignore()
        except:
            logging.debug('qt5, closeEvent : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))    

    def Update_L(self, data_payload, option, location):
        try:
            if(location == "G00"):
                if (option == 1):
                    if (float(data_payload['NODE23']['value']) <= CONSTANT.L['min']):
                        self.app.tab1_l1.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE23']['value']) >= CONSTANT.L['max']):
                        self.app.tab1_l1.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_l1.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_l1.setText(str(data_payload['NODE23']['value'] ))
                else:
                    pass
            elif(location == "G01"):
                if(option == 2):
                    if (float(data_payload['NODE24']['value'])  <= CONSTANT.L['min']):
                        self.app.tab1_l2.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE24']['value'])  >= CONSTANT.L['max']):
                        self.app.tab1_l2.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_l2.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_l2.setText(str(data_payload['NODE24']['value'] ))
                else:
                    pass
            else:
                pass
        except:
            logging.debug('qt5, Update_L : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

# PH

    def Update_PH(self, data_payload, option, location):
        try:
            if(location == "G00"):
                if (option == 1):
                    if (float(data_payload['NODE32']['value']) <= CONSTANT.PH['min']):
                        self.app.tab1_ph1.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE32']['value']) >= CONSTANT.PH['max']):
                        self.app.tab1_ph1.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_ph1.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_ph1.setText(str(data_payload['NODE32']['value']))
                else:
                    pass
            elif(location == "G01"):
                if(option == 2):
                    if (float(data_payload['NODE33']['value']) <= CONSTANT.PH['min']):
                        self.app.tab1_ph2.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE33']['value']) >= CONSTANT.PH['max']):
                        self.app.tab1_ph2.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_ph2.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_ph2.setText(str(data_payload['NODE33']['value']))
                else:
                    pass
            else:
                pass
        except:
            logging.debug('qt5, Update_PH : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

# Nhiệt độ

    def Update_T(self, data_payload, option, location):
        try:
            if(location == "G00"):
                if (option == 1):
                    if (float(data_payload['NODE25']['value']) <= CONSTANT.T['min']):
                        self.app.tab1_t1.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE25']['value']) >= CONSTANT.T['max']):
                        self.app.tab1_t1.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_t1.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_t1.setText(str(data_payload['NODE25']['value']))
                else:
                    pass
            elif(location == "G01"):
                if (option == 2):
                    if (float(data_payload['NODE26']['value']) <= CONSTANT.T['min']):
                        self.app.tab1_t2.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE26']['value']) >= CONSTANT.T['max']):
                        self.app.tab1_t2.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_t2.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_t2.setText(str(data_payload['NODE26']['value']))
                else:
                    pass
            else:
                pass
        except:
            logging.debug('qt5, Update_T : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  
# Độ ẩm KK

    def Update_H(self, data_payload, option, location):
        try:
            if(location == "G00"):
                if (option == 1):
                    if (float(data_payload['NODE21']['value'])<= CONSTANT.H['min']):
                        self.app.tab1_h1.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE21']['value']) >= CONSTANT.H['max']):
                        self.app.tab1_h1.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_h1.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_h1.setText(str(data_payload['NODE21']['value']))
                else:
                    pass
            elif(location == "G01"):
                if(option == 2):
                    if (float(data_payload['NODE22']['value']) <= CONSTANT.H['min']):
                        self.app.tab1_h2.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE22']['value']) >= CONSTANT.H['max']):
                        self.app.tab1_h2.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_h2.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_h2.setText(str(data_payload['NODE22']['value']))
                else:
                    pass
            else:
                pass
        except:
            logging.debug('qt5, Update_H : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

# Độ ẩm Đất

    def Update_SM(self, data_payload, option, location):
        try:
            if(location == "G00"):
                if (option == 1):
                    if (float(data_payload['NODE1']['value']) <= CONSTANT.SM['min']):
                        self.app.tab1_sm1.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE1']['value']) >= CONSTANT.SM['max']):
                        self.app.tab1_sm1.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm1.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm1.setText(str(data_payload['NODE1']['value'] ))

                if (option == 2):
                    if (float(data_payload['NODE2']['value']) <= CONSTANT.SM['min']):
                        self.app.tab1_sm2.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE2']['value'])  >= CONSTANT.SM['max']):
                        self.app.tab1_sm2.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm2.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm2.setText(str(data_payload['NODE2']['value'] ))

                if (option == 3):
                    if (float(data_payload['NODE3']['value']) <= CONSTANT.SM['min']):
                        self.app.tab1_sm3.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE3']['value'])  >= CONSTANT.SM['max']):
                        self.app.tab1_sm3.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm3.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm3.setText(str(data_payload['NODE3']['value'] ))

                if (option == 4):
                    if (float(data_payload['NODE4']['value'])  <= CONSTANT.SM['min']):
                        self.app.tab1_sm4.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE4']['value'] ) >= CONSTANT.SM['max']):
                        self.app.tab1_sm4.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm4.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm4.setText(str(data_payload['NODE4']['value'] ))

                if (option == 5):
                    if (float(data_payload['NODE5']['value'] ) <= CONSTANT.SM['min']):
                        self.app.tab1_sm5.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE5']['value'])  >= CONSTANT.SM['max']):
                        self.app.tab1_sm5.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm5.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm5.setText(str(data_payload['NODE5']['value'] ))

                if (option == 6):
                    if (float(data_payload['NODE6']['value'])  <= CONSTANT.SM['min']):
                        self.app.tab1_sm6.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE6']['value'] ) >= CONSTANT.SM['max']):
                        self.app.tab1_sm6.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm6.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm6.setText(str(data_payload['NODE6']['value'] ))

                if (option == 7):
                    if (float(data_payload['NODE7']['value'] ) <= CONSTANT.SM['min']):
                        self.app.tab1_sm7.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE7']['value']) >= CONSTANT.SM['max']):
                        self.app.tab1_sm7.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm7.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm7.setText(str(data_payload['NODE7']['value'] ))

                if (option == 8):
                    if (float(data_payload['NODE8']['value'])  <= CONSTANT.SM['min']):
                        self.app.tab1_sm8.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE8']['value'] ) >= CONSTANT.SM['max']):
                        self.app.tab1_sm8.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm8.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm8.setText(str(data_payload['NODE8']['value'] ))

                if (option == 9):
                    if (float(data_payload['NODE9']['value'])  <= CONSTANT.SM['min']):
                        self.app.tab1_sm9.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE9']['value'] ) >= CONSTANT.SM['max']):
                        self.app.tab1_sm9.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm9.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm9.setText(str(data_payload['NODE9']['value'] ))

                if (option == 10):
                    if (float(data_payload['NODE10']['value']) <= CONSTANT.SM['min']):
                        self.app.tab1_sm10.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE10']['value'])  >= CONSTANT.SM['max']):
                        self.app.tab1_sm10.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm10.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm10.setText(str(data_payload['NODE10']['value'] ))
                else:
                    pass

            elif(location == "G01"):
                if (option == 11):
                    if (float(data_payload['NODE11']['value'])  <= CONSTANT.SM['min']):
                        self.app.tab1_sm11.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE11']['value'])  >= CONSTANT.SM['max']):
                        self.app.tab1_sm11.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm11.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm11.setText(str(data_payload['NODE11']['value'] ))

                if (option == 12):
                    if (float(data_payload['NODE12']['value'])  <= CONSTANT.SM['min']):
                        self.app.tab1_sm12.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE12']['value'] ) >= CONSTANT.SM['max']):
                        self.app.tab1_sm12.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm12.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm12.setText(str(data_payload['NODE12']['value'] ))

                if (option == 13):
                    if (float(data_payload['NODE13']['value'])  <= CONSTANT.SM['min']):
                        self.app.tab1_sm13.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE13']['value'] ) >= CONSTANT.SM['max']):
                        self.app.tab1_sm13.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm13.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm13.setText(str(data_payload['NODE13']['value'] ))

                if (option == 14):
                    if (float(data_payload['NODE14']['value']) <= CONSTANT.SM['min']):
                        self.app.tab1_sm14.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE14']['value']) >= CONSTANT.SM['max']):
                        self.app.tab1_sm14.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm14.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm14.setText(str(data_payload['NODE14']['value']))

                if (option == 15):
                    if (float(data_payload['NODE15']['value']) <= CONSTANT.SM['min']):
                        self.app.tab1_sm15.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE15']['value']) >= CONSTANT.SM['max']):
                        self.app.tab1_sm15.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm15.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm15.setText(str(data_payload['NODE15']['value']))

                if (option == 16):
                    if (float(data_payload['NODE16']['value']) <= CONSTANT.SM['min']):
                        self.app.tab1_sm16.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE16']['value'])>= CONSTANT.SM['max']):
                        self.app.tab1_sm16.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm16.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm16.setText(str(data_payload['NODE16']['value']))

                if (option == 17):
                    if (float(data_payload['NODE17']['value'] )<= CONSTANT.SM['min']):
                        self.app.tab1_sm17.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE17']['value']) >= CONSTANT.SM['max']):
                        self.app.tab1_sm17.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm17.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm17.setText(str(data_payload['NODE17']['value']))

                if (option == 18):
                    if (float(data_payload['NODE18']['value']) <= CONSTANT.SM['min']):
                        self.app.tab1_sm18.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE18']['value']) >= CONSTANT.SM['max']):
                        self.app.tab1_sm18.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm18.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm18.setText(str(data_payload['NODE18']['value']))

                if (option == 19):
                    if (float(data_payload['NODE19']['value']) <= CONSTANT.SM['min']):
                        self.app.tab1_sm19.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE19']['value']) >= CONSTANT.SM['max']):
                        self.app.tab1_sm19.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm19.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm19.setText(str(data_payload['NODE19']['value']))

                if (option == 20):
                    if (float(data_payload['NODE20']['value']) <= CONSTANT.SM['min']):
                        self.app.tab1_sm20.setStyleSheet(
                            "QLabel {color:rgb(0, 0, 255);background-color: rgb(255, 255, 255)}")
                    elif (float(data_payload['NODE20']['value']) >= CONSTANT.SM['max']):
                        self.app.tab1_sm20.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0);background-color: rgb(255, 255, 255)}")
                    else:
                        self.app.tab1_sm20.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0);background-color: rgb(255, 255, 255)}")
                    self.app.tab1_sm20.setText(str(data_payload['NODE20']['value']))
                else:
                    pass
            else:
                pass
        except:
            logging.debug('qt5, Update_SM : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

    def Update_RF_Relay(self, data_payload):
        try:
            if(data_payload["NODE27"]["RF_signal"] == "Perfect"):
                self.app.tab2_th1.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0); font: 14pt 'MS Shell Dlg 2'}")
            elif(data_payload["NODE27"]["RF_signal"] == "Good"):
                self.app.tab2_th1.setStyleSheet(
                            "QLabel {color:rgb(131, 199, 93)}")
            elif(data_payload["NODE27"]["RF_signal"] == "Medium"):
                self.app.tab2_th1.setStyleSheet(
                            "QLabel {color:rgb(255, 255, 0)}")
            elif(data_payload["NODE27"]["RF_signal"] == "Bad"):
                self.app.tab2_th1.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0)}")
            else:
                pass
        
            if(data_payload["NODE27"]["RF_signal"] == 0):
                self.app.tab2_th1.setText("NULL")
            else:
                self.app.tab2_th1.setText(str(data_payload["NODE27"]["RF_signal"]))



            if(data_payload["NODE28"]["RF_signal"] == "Perfect"):
                self.app.tab2_th2.setStyleSheet(
                            "QLabel {color:rgb(0, 255, 0); font: 14pt 'MS Shell Dlg 2'}")
            elif(data_payload["NODE28"]["RF_signal"] == "Good"):
                self.app.tab2_th2.setStyleSheet(
                            "QLabel {color:rgb(131, 199, 93)}")
            elif(data_payload["NODE28"]["RF_signal"] == "Medium"):
                self.app.tab2_th2.setStyleSheet(
                            "QLabel {color:rgb(255, 255, 0)}")
            elif(data_payload["NODE28"]["RF_signal"] == "Bad"):
                self.app.tab2_th2.setStyleSheet(
                            "QLabel {color:rgb(255, 0, 0)}")
            else:
                pass
            if(data_payload["NODE28"]["RF_signal"] == 0):
                self.app.tab2_th2.setText("NULL")
            else:
                self.app.tab2_th2.setText(str(data_payload["NODE28"]["RF_signal"]))

            # self.app.tab2_th3.setText("TÍN HIỆU" + str(data_payload["NODE29"]["RF_signal"]))
            # self.app.tab2_th4.setText("TÍN HIỆU" + str(data_payload["NODE30"]["RF_signal"]))
            # self.app.tab2_th5.setText("TÍN HIỆU" + str(data_payload["NODE31"]["RF_signal"]))
        except:
            logging.debug('qt5, Update_RF_Relay : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

    def check_internet(self):
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            socket.create_connection(("www.google.com", 80), 2)
            return True
        except:
            return False

    def display_internet(self, option):
        try: 
            if (option == 1):
                self.app.lbl_internet.hide()

            else:
                self.app.lbl_internet.show()
                self.app.lbl_internet.setStyleSheet(
                    "QLabel {color: red; border-radius: 9px;   border: 2px solid red}")
                self.app.lbl_internet.setText("KHÔNG CÓ INTERNET")
        except:
            logging.debug('qt5, display_internet : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))             

    def chang_status_RL(self, device, status):
        try:
            if (device == 1):
                if (status == 1):
                    self.app.tab2_img_1.setPixmap(QtGui.QPixmap(
                        "photos\\dieu_khien_thiet_bi\\wplum_on.png"))
                    self.app.tab2_btn_r1on.setStyleSheet(
                        "QPushButton {background-color: rgb(0, 170, 0);}")
                    self.app.tab2_btn_r1off.setStyleSheet(
                        "QPushButton {background-color: rgb(229, 229, 229);}")
                elif (status == 0):
                    self.app.tab2_img_1.setPixmap(QtGui.QPixmap(
                        "photos\\dieu_khien_thiet_bi\\wplum_off.jpg"))        
                    self.app.tab2_btn_r1on.setStyleSheet(
                        "QPushButton {background-color: rgb(229, 229, 229);}")
                    self.app.tab2_btn_r1off.setStyleSheet(
                        "QPushButton {background-color: rgb(255, 0, 0);}")
                else:
                    pass
            elif (device == 2):
                if (status == 1):
                    self.app.tab2_img_2.setPixmap(QtGui.QPixmap(
                        "photos\\dieu_khien_thiet_bi\\curtain_on.png"))
                    self.app.tab2_btn_r2on.setStyleSheet(
                            "QPushButton {background-color: rgb(0, 170, 0);}")
                    self.app.tab2_btn_r2off.setStyleSheet(
                            "QPushButton {background-color: rgb(229, 229, 229);}")

                elif (status == 0):
                    self.app.tab2_img_2.setPixmap(QtGui.QPixmap(
                        "photos\\dieu_khien_thiet_bi\\curtain_off.png"))
                    self.app.tab2_btn_r2on.setStyleSheet(
                            "QPushButton {background-color: rgb(229, 229, 229);}")
                    self.app.tab2_btn_r2off.setStyleSheet(
                            "QPushButton {background-color: rgb(255, 0, 0);}")
                else:
                    pass
            else:
                pass
        except:
            logging.debug('qt5, chang_status_RL : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

    def UpdatePicture(self, device, status): # update picture when press
        try:
            if(device == 1):
                if(status == 1):    # relay1 on
                    self.chang_status_RL(1, 1)
                elif(status == 0):  # relay1 off
                    self.chang_status_RL(1, 0)
                    # khi mà counter ấn off - dừng luôn

                    if(CONSTANT.SubThread_pump1.isActive()):
                        CONSTANT.SubThread_pump1.stop() # dừng bơm lại
                        CONSTANT.flag_pump1   = 0   #trở về trạng thái bắt đầu
                        CONSTANT.flag_pump1_N = 1
                        CONSTANT.TIME["pump1"]["minute"] = 2    # cập nhập lại biến time
                        CONSTANT.TIME["pump1"]["second"] = 0
                        self.app.lcdNumber.hide() 
                else:
                    pass
            elif(device == 2):
                if(status == 1):   
                    self.chang_status_RL(2, 1)
                elif(status == 0):
                    self.chang_status_RL(2, 0)

                    if(CONSTANT.SubThread_curtain1.isActive()):
                        CONSTANT.SubThread_curtain1.stop() # dừng bơm lại
                        CONSTANT.flag_curtain1 = 0 
                        CONSTANT.flag_curtain1_N = 1
                        CONSTANT.TIME["curtain1"]["minute"] = 2    # cập nhập lại biến time
                        CONSTANT.TIME["curtain1"]["second"] = 0
                        self.app.lcdNumber_2.hide() 
                else:
                    pass
            else:
                pass
        except:
            logging.debug('qt5, UpdatePicture : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))     


    # format 5:00 - time = ("{0}:{1}".format(m,s))
    def LCD_Number(self):
        try:
            self.app.lcdNumber.hide()
            self.app.lcdNumber_2.hide()
            self.app.lcdNumber_3.hide()
            self.app.lcdNumber_4.hide()
            self.app.lcdNumber_5.hide()
        except:
            logging.debug('qt5, LCD_Number : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))) 

    def countdown_pump1(self):
        try: 
            if (CONSTANT.TIME["pump1"]["second"] > 0):
                CONSTANT.TIME["pump1"]["second"] -= 1
            else:
                if (CONSTANT.TIME["pump1"]["minute"] > 0):
                    CONSTANT.TIME["pump1"]["minute"]  -= 1
                    CONSTANT.TIME["pump1"]["second"] = 59
                elif((CONSTANT.TIME["pump1"]["minute"] ==0) and (CONSTANT.TIME["pump1"]["second"]==0)):
                    self.app.lcdNumber.hide() 
                    CONSTANT.SubThread_pump1.stop() # dừng bơm lại
                    CONSTANT.flag_pump1 = 0 
                    CONSTANT.flag_pump1_N = 0
                    return 
                else:
                    pass 
            time = ("{0}:{1}".format(CONSTANT.TIME["pump1"]["minute"] , CONSTANT.TIME["pump1"]["second"])) 

            self.app.lcdNumber.show()
            self.app.lcdNumber.setDigitCount(len(time))
            self.app.lcdNumber.display(time)
        except:
            logging.debug('qt5, countdown_pump1 : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))            

    def countdown_curtain1(self):
        try:
            if CONSTANT.TIME["curtain1"]["second"] > 0:
                CONSTANT.TIME["curtain1"]["second"]  -=1
            else:
                if CONSTANT.TIME["curtain1"]["minute"]  > 0:
                    CONSTANT.TIME["curtain1"]["minute"] -= 1
                    CONSTANT.TIME["curtain1"]["second"]  = 59
                elif((CONSTANT.TIME["curtain1"]["minute"] ==0) and (CONSTANT.TIME["curtain1"]["second"] ==0)):
                    self.app.lcdNumber_2.hide() 
                    CONSTANT.SubThread_curtain1.stop() # dừng bơm lại
                    CONSTANT.flag_curtain1 = 0 
                    CONSTANT.flag_curtain1_N = 0
                    return
                else:
                    pass 
            time = ("{0}:{1}".format(CONSTANT.TIME["curtain1"]["minute"] , CONSTANT.TIME["curtain1"]["second"] )) 
            self.app.lcdNumber_2.show()
            self.app.lcdNumber_2.setDigitCount(len(time))
            self.app.lcdNumber_2.display(time)
        except:
            logging.debug('qt5, countdown_curtain1 : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))    