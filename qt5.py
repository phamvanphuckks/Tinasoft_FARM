from PyQt5           import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QInputDialog, QAction, QGroupBox, QTableWidget, QTableWidgetItem, QWidget, QMessageBox
from PyQt5.QtCore    import QTimer, QTime, QThread, pyqtSignal, Qt, QObject
from PyQt5.QtGui     import QPixmap, QCloseEvent, QColor

import constant  as CONSTANT
import sys, socket, logging
from datetime import datetime

logging.basicConfig(filename='logs\\error_code.log',level=logging.INFO)

class qt5Class(QtCore.QObject):

    def __init__(self):
        try:
            QtCore.QObject.__init__(self)
            self.App = QtWidgets.QApplication([])
            self.app = uic.loadUi("guis\\main.ui")
            self.app.closeEvent = self.closeEvent # khi close, gọi sự kiện closeEvent
            self.initialize()
        except:
            logging.info('qt5, __init__ : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))               

    def infog(self, error, information):
        try:
            QMessageBox.critical(self.app, error, information)
        except:
            logging.info('qt5, infog : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))    

    def initialize(self): # khi mình khởi động off hết
        try: 
            for i in range(1, 6):
                self.UpdatePicture(i, 0)
            if(self.check_internet()== True):
                self.display_internet(1)
            else:
                self.display_internet(0)
        except:
            logging.info('qt5, initialize : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))    

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
            logging.info('qt5, closeEvent : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))    

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
            logging.info('qt5, Update_L : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

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
            logging.info('qt5, Update_PH : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

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
            logging.info('qt5, Update_T : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  
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
            logging.info('qt5, Update_H : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

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
            logging.info('qt5, Update_SM : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

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
                self.app.tab2_th1.setText("NULL")

            self.app.tab2_th1.setText(str(data_payload["NODE27"]["RF_signal"]))
            if(data_payload["NODE27"]["RF_signal"] == 0):
                self.app.tab2_th1.setText("NULL")

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
                self.app.tab2_th2.setText("NULL")

            self.app.tab2_th2.setText(str(data_payload["NODE28"]["RF_signal"]))
            if(data_payload["NODE28"]["RF_signal"] == 0):
                self.app.tab2_th2.setText("NULL")
        except:
            logging.info('qt5, Update_RF_Relay : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

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
            logging.info('qt5, display_internet : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))             

    def chang_status_RL(self, device, status, channel = 1):
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
                    if(channel == 1):
                        self.app.tab2_img_2.setPixmap(QtGui.QPixmap(
                            "photos\\dieu_khien_thiet_bi\\curtain_on.png"))
                        self.app.tab2_btn_r2on.setStyleSheet(
                                "QPushButton {background-color: rgb(0, 170, 0);}")
                        self.app.tab2_btn_r2off.setStyleSheet(
                                "QPushButton {background-color: rgb(229, 229, 229);}")
                    elif(channel == 2):
                        self.app.tab2_img_2.setPixmap(QtGui.QPixmap(
                            "photos\\dieu_khien_thiet_bi\\curtain_on.png"))
                        self.app.tab2_btn_r2on.setStyleSheet(
                                "QPushButton {background-color: rgb(229, 229, 229);}")
                        self.app.tab2_btn_r2off.setStyleSheet(
                                "QPushButton {background-color: rgb(0, 170, 0);}")                                
                elif (status == 0):
                    self.app.tab2_img_2.setPixmap(QtGui.QPixmap(
                        "photos\\dieu_khien_thiet_bi\\curtain_off.png"))
                    self.app.tab2_btn_r2on.setStyleSheet(
                            "QPushButton {background-color: rgb(229, 229, 229);}")
                    self.app.tab2_btn_r2off.setStyleSheet(
                            "QPushButton {background-color: rgb(229, 229, 229);}")
                else:
                    pass
            else:
                pass
        except:
            logging.info('qt5, chang_status_RL : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

    def UpdatePicture(self, device, status, channel = 1): # update picture when press
        try:
            if(device == 1):
                if(status == 1):    # relay1 on
                    self.chang_status_RL(1, 1)
                elif(status == 0):  # relay1 off
                    self.chang_status_RL(1, 0)
                else:
                    pass
            elif(device == 2):
                if(status == 1):   
                    self.chang_status_RL(2, 1, channel)
                elif(status == 0):
                    self.chang_status_RL(2, 0, channel)
                else:
                    pass
            else:
                pass
        except:
            logging.info('qt5, UpdatePicture : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))     