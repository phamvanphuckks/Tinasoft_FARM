from PyQt5.QtWidgets import QVBoxLayout, QAction, QGroupBox, QTableWidget, QTableWidgetItem, QWidget, QMessageBox
from PyQt5.QtCore    import QTimer, QTime, QThread, pyqtSignal
from PyQt5           import QtCore, QtGui
from datetime        import datetime   # date_time

import sys, time, json, socket    # library in python
import requests                   # api

import serial
import serial.tools.list_ports
import paho.mqtt.client as mqtt # mqtt

# library programer development
import constant     as  CONSTANT
import db_handler   as  SQLite

from gateway    import Gateway
from qt5        import qt5Class

import random, logging

import threading

# define globale
Windowns = qt5Class()
DB       = SQLite.DataBase()

'''
---------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------
'''

logging.basicConfig(filename='logs\\error_code.log',level=logging.DEBUG)

#--define MQTT--------------------------------------
MQTT_HOST = 'smartfarm.tinasoft.com.vn'
MQTT_USER = 'smartFarm'
MQTT_PWD  = 'Smartktdt1@123!'
MQTT_TOPIC_SEND    = 'send_data'
MQTT_TOPIC_CONTROL = 'controller'
MQTT_TOPIC_STATUS  = 'control_status'


def Init_mqtt():
    global client
    try: 
        if(check_internet() == True):
            try:
                client = mqtt.Client()
                client.username_pw_set(MQTT_USER, MQTT_PWD)
                client.connect(MQTT_HOST, 1883)
                client.on_connect = on_connect
                client.on_message = on_message
                client.loop_start()
                get_status_all()
            except:
                logging.debug('Khoi tao Mqtt error - mqtt error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))                
        else:
            logging.debug('Khoi tao Mqtt error - khong co internet: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    except:
        logging.debug('Init_mqtt error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

#--end--------------------------------------------------------------------------------------------------------


#---controller device------------------------------------------------------------------------------------------
'''
+ hàm điểu khiển thiết bị
    + UpdatePicture() trong file qt5.py,  
    + control_RL() trong file gateway_v1.py
    + get_status() : gửu message trạng thái của relay lên server
'''
def ControlDevice(device, status): # kiêu kiểu thế này
    try:
        # kiểm tra nếu mà khi đồng bộ thì không cho bấm nút
        if(CONSTANT.Flag_Update_Syn_Button == False):
            if (device == 1):  # pump1
                if(status == 1):
                    GW_Blue.control_RL(23, 1, 1) # GateWay(Xanh) điểu khiển Relay 
                    Windowns.UpdatePicture(device, status) # thay đổi trên app 
                    if(get_status(27) == "1"):
                        Windowns.UpdatePicture(device, status) # thay đổi trên app  
                        #print("RELAY1 ON") 
                elif(status == 0):
                    GW_Blue.control_RL(23, 1, 0)
                    Windowns.UpdatePicture(device, status) # thay đổi trên app 
                    if(get_status(27) == "0"):
                        Windowns.UpdatePicture(device, status)
                        #print("RELAY1 OFF") 
                else:
                    pass
            elif(device == 2): # curtain1
                if(status == 1):
                    GW_Blue.control_RL(24, 1, 1) # GateWay(Xanh) điểu khiển Relay 
                    Windowns.UpdatePicture(device, status) # thay đổi trên app 
                    if(get_status(28) == "1"):
                        Windowns.UpdatePicture(device, status) # thay đổi trên app
                        # print("RELAY2 ON") 
                elif(status == 0):
                    GW_Blue.control_RL(24, 1, 0)
                    Windowns.UpdatePicture(device, status) # thay đổi trên app 
                    if(get_status(28) == "0"):
                        Windowns.UpdatePicture(device, status)
                        # print("RELAY2 OFF") 
                else:
                    pass
            else:
                pass
        else:
            if((device == 1) or(device == 2)):
                payload_data = {
                    'sub_id': "G00",
                    'date_sync'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'status': "False"
                }
            else:
                pass
            
            if(check_internet() == True):
                try:
                    client.publish(MQTT_TOPIC_STATUS, json.dumps(payload_data))
                except:
                    logging.debug('Loi publish MQTT_TOPIC_STATUS , Control_device  - mqtt error : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            else:
                logging.debug('Loi publish MQTT_TOPIC_STATUS , Control_device - khong co mang : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))                
    except:
        logging.debug('ControlDevice error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

'''
    + lấy trạng thái của tất cả thiết bị relay
    + Init_mqtt() gọi function này : cập nhập lại button khi mất mạng và khi khởi động hệ thống
'''
def get_status_all(): # lấy trạng thái hiện tại của thiet bi
    global client, GW_Blue
    try:
        # Relay trang trai G00
        payload_dataG00 = {
            'sub_id'     : "G00",
            'date_sync'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'time'       : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "relay_1": {
                "RF_signal": GW_Blue.get_RFsignal(23),
                'value'    : str(GW_Blue.get_status_RL(23, 1)),
                'battery'  : 100,
            },

            "relay_2": {
                "RF_signal": GW_Blue.get_RFsignal(24),
                'value'    : str(GW_Blue.get_status_RL(24, 1)),
                'battery'  : 100
            }
        }

        # chỉ điều khiển thiết bị G00 - Mái che và Máy bơm
        if (check_internet() == True): 
            try:
                client.publish(MQTT_TOPIC_STATUS, json.dumps(payload_dataG00))
                # print("get status all")
                # print(json.dumps(payload_dataG00))
            except:
                logging.debug('Loi Publish get_status_all - mqtt error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            logging.debug('Loi Publish get_status_all - Khong co Internet : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    except:
        logging.debug('get_status_all error : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


'''
    + lấy trạng thái của từng relay
'''
def get_status(pos): 
    try:
        global client, GW_Blue
        # 1 nong trai se co 2 relay Relay_1 va relay_2
        if(pos == 27):
            CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"]     = str(GW_Blue.get_status_RL(23, 1))
            CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"] = GW_Blue.get_RFsignal(23, CONSTANT.SENSOR["relay"])
            CONSTANT.DATA_RELAY["NODE" + str(pos)]["id"]        = GW_Blue.get_node_id(23, CONSTANT.SENSOR["relay"])
            Windowns.Update_RF_Relay(CONSTANT.DATA_RELAY)
            payload_data = {
                'sub_id': "G00",
                'date_sync'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "relay_1": {
                    "RF_signal": CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"],
                    'value':     str(CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"]),
                    'battery': 100
                }
            }
        elif(pos == 28):
            CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"]     = str(GW_Blue.get_status_RL(24, 1))
            CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"] = GW_Blue.get_RFsignal(24, CONSTANT.SENSOR["relay"])
            CONSTANT.DATA_RELAY["NODE" + str(pos)]["id"]        = GW_Blue.get_node_id(24, CONSTANT.SENSOR["relay"])
            Windowns.Update_RF_Relay(CONSTANT.DATA_RELAY)

            payload_data = {
                'sub_id': "G00",
                'date_sync'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "relay_2": {
                    "RF_signal": CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"],
                    'value':    str(CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"]),
                    'battery': 100
                }
            }
        else:
            pass
        
        # publish message to server and insert database controller
        if(check_internet() == True): 
            DB.insert_data_row("controller", pos, CONSTANT.DATA_RELAY["NODE" + str(pos)]["name"], CONSTANT.DATA_RELAY["NODE" + str(pos)]["id"],
            CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"], CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"], 100, 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "ok")
            # print("get status")
            try:
                client.publish(MQTT_TOPIC_STATUS, json.dumps(payload_data))
                # print(json.dumps(payload_data))
            except:
                logging.debug('Loi publish get_status - mqtt error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))        

        else:
            DB.insert_data_row("controller", pos, CONSTANT.DATA_RELAY["NODE" + str(pos)]["name"],CONSTANT.DATA_RELAY["NODE" + str(pos)]["id"],
            CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"], CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"], 100, 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "error")

            logging.debug('khong co Internet, get_status ghi vao Database : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        return CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"]
    
    except:
        logging.debug('get_status error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))   

def on_connect(client, userdata, flags, rc):    # subscrie on  topic
    # print("Connected with result code " + str(rc))
    try:
        client.subscribe(MQTT_TOPIC_CONTROL)
    except:
        logging.debug('subscribe topic error : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

def on_message(client, userdata, msg):  # received data - chua code xong
    # print(msg.topic+" "+str(msg.payload))
    try:
        data = json.loads(msg.payload.decode('utf-8'))

        if(CONSTANT.Flag_Update == False):
            if(data['sub_id'] == "G00"):
                if ("relay_1" in data): 
                    if (data['relay_1']['value'] == '1'):

                        ControlDevice(1, 1)
                    if (data['relay_1']['value'] == '0'):

                        ControlDevice(1, 0)
                if ("relay_2" in data):
                    if (data['relay_2']['value'] == '1'):
                        ControlDevice(2, 1)
                    if (data['relay_2']['value'] == '0'):
                        ControlDevice(2, 0)

            if(data['sub_id'] == "G01"):
                if ("relay_1" in data): 
                    if (data['relay_1']['value'] == '1'):
                        ControlDevice(3, 1)
                    if (data['relay_1']['value'] == '0'):
                        ControlDevice(3, 0)
                if ("relay_2" in data):
                    if (data['relay_2']['value'] == '1'):
                        ControlDevice(4, 1)
                    if (data['relay_2']['value'] == '0'):
                        ControlDevice(4, 0)
        else:
            payload_data = {
                'sub_id': data['sub_id'],
                'date_sync'  : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': "False"
            }
            if(check_internet() == True):
                try:
                    client.publish(MQTT_TOPIC_STATUS, json.dumps(payload_data))
                    # print("False False False")
                except:
                    logging.debug('Loi publish MQTT_TOPIC_STATUS, on_message - mqtt error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))) 
            else:
                logging.debug('Loi publish MQTT_TOPIC_STATUS, on_message - khong co Internet : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))    
    except:
        logging.debug('Loi on_message : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))          


def Init_Button():
    try:
        Windowns.app.tab2_btn_r1off.clicked.connect(lambda:ControlDevice(1, 0))
        Windowns.app.tab2_btn_r1on.clicked.connect(lambda:ControlDevice(1, 1))

        Windowns.app.tab2_btn_r2off.clicked.connect(lambda:ControlDevice(2, 0))
        Windowns.app.tab2_btn_r2on.clicked.connect(lambda:ControlDevice(2, 1))

    except:
        logging.debug('Init_Button Error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))   

#---end ----------------------------------------------------------------------------------------------------------

#--- Update Data--------------------------------------------------------------------------------------------------
def Init_UI(): # khởi tạo GateWay_Xanh
    global GW_Blue

    ports = serial.tools.list_ports.comports()
    check_device = ''

    if(len(ports) > 0): # khởi tạo để kết nối với GateWay(Xanh)
        for port in ports:
            # print(port)
            if ("USB-SERIAL CH340" in str(port)):
                check_device = port.device
                break
        if (check_device != ''):
            GW_Blue = Gateway(CONSTANT.GW_Blue_NAME)   #Define GW_Blue kế thừa CONSTANT.GW_Blue_NAME
            # print("Da ket noi GateWay")
        else:
            QMessageBox.critical(Windowns.app, "LỖI KẾT NỐI",
                                      "KHÔNG ĐÚNG THIẾT BỊ")
            logging.debug('Khoi tao UI error : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            sys.exit()
    else:
        QMessageBox.critical(Windowns.app, "LỖI KẾT NỐI",
                                  "KHÔNG CÓ COM NÀO ĐƯỢC KẾT NỐI")
        logging.debug('Khoi tao UI error : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        sys.exit()

def check_internet():   # kiểm tra internet
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80), 1)
        return True
    except:
        return False

def requirePort(): # Xac dinh COM 
    try:
        file = open("port\\port.txt", "r")
        CONSTANT.GW_Blue_NAME = file.read(4)
        # Đóng file
        file.close()
    except:
        logging.debug('requirePort error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))   

#---end-----------------------------------------------------------------------------------------------------------



#---define thread-------------------------------------------------------------------------------------------------
# 0 1 -  khoi dau
# 0 0 -  dung
# 1 1 -  chay
# 1 0 -  reserve

def check_pump1():
    try:
        if( 
            (float(CONSTANT.DATA_G00["NODE1"]["value"]) < int(CONSTANT.SM["min"]) ) and   
            (float(CONSTANT.DATA_G00["NODE2"]["value"]) < int(CONSTANT.SM["min"]) ) and
            (float(CONSTANT.DATA_G00["NODE2"]["value"]) < int(CONSTANT.SM["min"]) )
        ):
            return True
        else:
            return False
    except:
        logging.debug('check_pump1 error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

def check_curtain1():
    try:
        if(float(CONSTANT.DATA_G00["NODE23"]["value"]) < int(CONSTANT.L["min"])):
            return True
        else:
            return False
    except:
        logging.debug('check_curtain1 error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

def Thread_pump1(): # flag_pump1 = 0 - chưa bật máy bơm, chưa đếm lùi - nếu flag_pump1 = 1 thì ko làm gì cả
    try:
        # bỏ cờ flag_pump1,flag_pump1_N=> khi mà điều kiện true. sẽ ra lệnh bệnh máy bơm nhiều lần
        if((CONSTANT.flag_pump1 == 0) and (CONSTANT.flag_pump1_N == 1)): 
            if((check_pump1()) and (CONSTANT.en_Relay == True)): # kiểm tra điều kiện- nhớ phải xét khoảng, 10< y 20<đây chưa xét khoảng
                CONSTANT.SubThread_pump1.start(1000) # bắt đầu đếm lui
                ControlDevice(1, 1)                 # Bật máy bơm
                CONSTANT.flag_pump1   = 1          
                CONSTANT.flag_pump1_N = 1
        elif((CONSTANT.flag_pump1 == 0) and (CONSTANT.flag_pump1_N == 0)):
            ControlDevice(1, 0)
            CONSTANT.TIME["pump1"]["minute"] = 2
            CONSTANT.TIME["pump1"]["second"] = 0
            CONSTANT.flag_pump1 = 0  
            CONSTANT.flag_pump1_N = 1
        else:
            pass
    except:
        logging.debug('Thread_pump1 error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

def Thread_curtain1():
    try:
        if((CONSTANT.flag_curtain1 == 0) and (CONSTANT.flag_curtain1_N == 1)):
            if((check_curtain1()) and (CONSTANT.en_Relay == True)): # kiểm tra điều kiện- nhớ phải xét khoảng, đây chưa xét khoảng
                CONSTANT.SubThread_curtain1.start(1000) # bắt đầu đếm lui
                ControlDevice(2, 1)                 # Bật máy bơm
                CONSTANT.flag_curtain1   = 1          
                CONSTANT.flag_curtain1_N = 1
        elif((CONSTANT.flag_curtain1 == 0) and (CONSTANT.flag_curtain1_N == 0)):
            ControlDevice(2, 0)
            CONSTANT.TIME["curtain1"]["minute"]  = 2
            CONSTANT.TIME["curtain1"]["second"]  = 0
            CONSTANT.flag_curtain1_N = 1
            CONSTANT.flag_curtain1   = 0

        else:
            pass
    except:
        logging.debug('Thread_curtain1 error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

#-----------------------------------------------------------------------------------------------------------------

def Thread_GatewayBlue():
    global GW_Blue, client
    try:
        # CONSTANT.en_Sensor : True  cho phép đọc cảm biến khi là ---- False không cho phép
        # CONSTANT.Flag_Update_Syn_Data :True : không cho phép đọc, False cho phép đọc
        if((CONSTANT.Flag_Update_Syn_Data == False)): #and (CONSTANT.en_Sensor == True)):
            logging.debug('Lay Data tu sensor Chu ky 120s : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            # print("Flage True")
            # Đang cập nhập dữ liệu từ GW
            CONSTANT.Flag_Update = True
            # đang đồng bộ dữ liệu
            # CONSTANT.Flag_Update_Syn_Data == True
            #soil moistrure
            for i in range(1, 11):
                CONSTANT.DATA_G00["NODE" + str(i)]["value"]        = str(GW_Blue.get_main_parameter(i, CONSTANT.SENSOR["soil_moistrure"]))
                CONSTANT.DATA_G00["NODE" + str(i)]["battery"]      = GW_Blue.get_battery(i, CONSTANT.SENSOR["soil_moistrure"])
                CONSTANT.DATA_G00["NODE" + str(i)]["RF_signal"]    = GW_Blue.get_RFsignal(i, CONSTANT.SENSOR["soil_moistrure"])
                CONSTANT.DATA_G00["NODE" + str(i)]["id"]           = GW_Blue.get_node_id(i, CONSTANT.SENSOR["soil_moistrure"])    
                CONSTANT.DATA_G00["NODE" + str(i)]["time"]         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
                    
            for i in range(11, 21):
                CONSTANT.DATA_G01["NODE" + str(i)]["value"]        = str(GW_Blue.get_main_parameter(i, CONSTANT.SENSOR["soil_moistrure"]))
                CONSTANT.DATA_G01["NODE" + str(i)]["battery"]      = GW_Blue.get_battery(i, CONSTANT.SENSOR["soil_moistrure"])
                CONSTANT.DATA_G01["NODE" + str(i)]["RF_signal"]    = GW_Blue.get_RFsignal(i, CONSTANT.SENSOR["soil_moistrure"])
                CONSTANT.DATA_G01["NODE" + str(i)]["id"]           = GW_Blue.get_node_id(i, CONSTANT.SENSOR["soil_moistrure"])
                CONSTANT.DATA_G01["NODE" + str(i)]["time"]         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")     

            # huminity
            CONSTANT.DATA_G00["NODE21"]["value"]        = int(GW_Blue.get_main_parameter(21, CONSTANT.SENSOR["humidity"]))
            CONSTANT.DATA_G00["NODE21"]["battery"]      = GW_Blue.get_battery(21, CONSTANT.SENSOR["humidity"])
            CONSTANT.DATA_G00["NODE21"]["RF_signal"]    = GW_Blue.get_RFsignal(21, CONSTANT.SENSOR["humidity"])
            CONSTANT.DATA_G00["NODE21"]["id"]           = GW_Blue.get_node_id(21, CONSTANT.SENSOR["humidity"])
            CONSTANT.DATA_G00["NODE21"]["time"]         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

            # light
            CONSTANT.DATA_G00["NODE23"]["value"]        = int(GW_Blue.get_main_parameter(22, CONSTANT.SENSOR["light"]))
            CONSTANT.DATA_G00["NODE23"]["battery"]      = GW_Blue.get_battery(22, CONSTANT.SENSOR["light"])
            CONSTANT.DATA_G00["NODE23"]["RF_signal"]    = GW_Blue.get_RFsignal(22, CONSTANT.SENSOR["light"])
            CONSTANT.DATA_G00["NODE23"]["id"]           = GW_Blue.get_node_id(22, CONSTANT.SENSOR["light"])   
            CONSTANT.DATA_G00["NODE23"]["time"]         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

            # Temperature
            CONSTANT.DATA_G00["NODE25"]["value"]        = int(GW_Blue.get_Temperature(1, CONSTANT.SENSOR["soil_moistrure"]))
            CONSTANT.DATA_G00["NODE25"]["battery"]      = GW_Blue.get_battery(1, CONSTANT.SENSOR["soil_moistrure"])
            CONSTANT.DATA_G00["NODE25"]["RF_signal"]    = GW_Blue.get_RFsignal(1, CONSTANT.SENSOR["soil_moistrure"])
            CONSTANT.DATA_G00["NODE25"]["id"]           = GW_Blue.get_node_id(1, CONSTANT.SENSOR["soil_moistrure"])   
            CONSTANT.DATA_G00["NODE25"]["time"]         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

            
            CONSTANT.DATA_G00["time"] = CONSTANT.DATA_G01["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # print("update GWblue")

            # update RF_signal relay
            CONSTANT.DATA_RELAY["NODE" + str(27)]["RF_signal"] = GW_Blue.get_RFsignal(23, CONSTANT.SENSOR["relay"])
            CONSTANT.DATA_RELAY["NODE" + str(28)]["RF_signal"] = GW_Blue.get_RFsignal(24, CONSTANT.SENSOR["relay"])

            # send message to server and insert database
            if(check_internet() == True): 
                try:
                    client.publish(MQTT_TOPIC_SEND, json.dumps(CONSTANT.DATA_G00)) 
                    client.publish(MQTT_TOPIC_SEND, json.dumps(CONSTANT.DATA_G01)) 
                    DB.insert_data_nongtraiG01("nongtrai_G01", "ok")  
                    DB.insert_data_nongtraiG00("nongtrai_G00", "ok")
                except:
                    logging.debug('Thread_GatewayBlue: Loi publish data G00, G01  - mqtt error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            else:
                try:
                    DB.insert_data_nongtraiG01("nongtrai_G01", "error") 
                    DB.insert_data_nongtraiG00("nongtrai_G00", "error") 
                except:
                    logging.debug('Thread_GatewayBlue: Loi publish data G00, G01  - khong co Internet : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            # cho phép thực hiện điều khiển
            CONSTANT.Flag_Update = False
            # Cho phép lấy dữ liệu
            # CONSTANT.Flag_Update_Syn_Data == False
            # có dữ liệu cập nhập
            # CONSTANT.Flag_Update_GUI  = False
            #print("Flag False")
        else:
            logging.debug('Thread_GatewayBlue: dang dong bo - khong cho phep Read sensor : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    except:
        logging.debug('Thread_GatewayBlue error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))   

def Thread_GatewayBlue_QT():
    try:
        Thread_GW  = threading.Thread(target=Thread_GatewayBlue, args=())
        Thread_GW.setDaemon(True)

        Thread_GW.start()
    except:
        logging.debug('Thread_GatewayBlue_QT error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

def Thread_UpdateGUI_QT():
    global Windowns
    try:
        # không truy xuất dữ liệu thì mới update Gui
        if(CONSTANT.Flag_Update_GUI  == False):

            for i in range(1, 11):
                Windowns.Update_SM(CONSTANT.DATA_G00, i, "G00")

            for i in range(11, 21):
                Windowns.Update_SM(CONSTANT.DATA_G01, i, "G01")

            Windowns.Update_H(CONSTANT.DATA_G00, 1, "G00")
            Windowns.Update_H(CONSTANT.DATA_G01, 2, "G01")

            Windowns.Update_L(CONSTANT.DATA_G00, 1, "G00")
            Windowns.Update_L(CONSTANT.DATA_G01, 2, "G01")

            Windowns.Update_T(CONSTANT.DATA_G00, 1, "G00")
            Windowns.Update_T(CONSTANT.DATA_G01, 2, "G01")

            # CONSTANT.DATA_RELAY["NODE27"]["RF_signal"]   = GW_Blue.get_RFsignal(23, CONSTANT.SENSOR["relay"])
            Windowns.Update_RF_Relay(CONSTANT.DATA_RELAY)
            # CONSTANT.Flag_Update_GUI  = False
    except:
        logging.debug('Thread_UpdateGUI_QT error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  
  

#--backup---------------------------------------------------------------------------------------------------------
def Synchronous():
    global client
    try:
        logging.debug('bat dau Synchronous  : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        # Không cho phép ghi vào database  và không cho phép lấy thêm dữ liệu
        CONSTANT.Flag_Update_Syn_Data = True
        # Không cho phép bấm nút
        CONSTANT.Flag_Update_Syn_Button = True

        CONSTANT.Flag_Update_GUI  = True

        Windowns.backup_Synchronous(1)
        max_G00   = DB.find_posMax("nongtrai_G00")
        max_G01   = DB.find_posMax("nongtrai_G01")
        max_Relay = DB.find_posMax("controller")

        # print("Synchronous begin")
        Init_mqtt()

        # print("off - 1")

        # NongtraiG00
        for i in range(1, max_G00 + 1):
            if(DB.check_syn("nongtrai_G00", i)==False): # phat hien ra la co data chua sync- vet tu day
                DB.update_data_row("nongtrai_G00", i, "ok")
                data = DB.get_data_row("nongtrai_G00", i)

                if(data!=[]):
                    CONSTANT.DATA_G00["NODE" + str(data[0][1])]["id"]        =  data[0][3]
                    CONSTANT.DATA_G00["NODE" + str(data[0][1])]["value"]     =  str(data[0][4])
                    CONSTANT.DATA_G00["NODE" + str(data[0][1])]["RF_signal"] =  data[0][5]   
                    CONSTANT.DATA_G00["NODE" + str(data[0][1])]["battery"]   =  data[0][6]    
                    # CONSTANT.DATA_G00["NODE" + str(data[0][1])]["time"]      =  data[0][7]
                    CONSTANT.DATA_G00["NODE" + str(data[0][1])]["syn"]       =  data[0][8]

                    if(i%14==0):
                        CONSTANT.DATA_G00["sub_id"] = "G00"
                        CONSTANT.DATA_G00["time"] = data[0][7]
                        #print(json.dumps(CONSTANT.DATA_G00))
                        if(check_internet() == True): 
                            try:
                                client.publish(MQTT_TOPIC_SEND, json.dumps(CONSTANT.DATA_G00))
                            except:
                                logging.debug('Synchronous: publish G00  mqtt error :' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        else:
                            logging.debug('Synchronous: khong co internet de publish G00 -khong co Internet :' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # print("off - 2")
        
        # NongtraiG01
        for i in range(1, max_G01 + 1):
            if(DB.check_syn("nongtrai_G01", i)==False): # phat hien ra la co data chua sync- vet tu day
                DB.update_data_row("nongtrai_G01", i, "ok")
                data = DB.get_data_row("nongtrai_G01", i)

                if(data!=[]):
                    CONSTANT.DATA_G01["NODE" + str(data[0][1])]["id"]        =  data[0][3]
                    CONSTANT.DATA_G01["NODE" + str(data[0][1])]["value"]     =  str(data[0][4])
                    CONSTANT.DATA_G01["NODE" + str(data[0][1])]["RF_signal"] =  data[0][5]   
                    CONSTANT.DATA_G01["NODE" + str(data[0][1])]["battery"]   =  data[0][6]    
                    # CONSTANT.DATA_G01["NODE" + str(data[0][1])]["time"]      =  data[0][7]
                    CONSTANT.DATA_G01["NODE" + str(data[0][1])]["syn"]       =  data[0][8]
                    if(i%14 == 0):
                        CONSTANT.DATA_G01["sub_id"] = "G01"
                        CONSTANT.DATA_G01["time"] = data[0][7]
                        # print(json.dumps(CONSTANT.DATA_G01))        
                        if(check_internet() == True): 
                            try:
                                client.publish(MQTT_TOPIC_SEND, json.dumps(CONSTANT.DATA_G01))
                            except:
                                logging.debug('Synchronous: publish G01 - mqtt error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        else:
                            logging.debug('Synchronous: khong co internet de publish G01  - Khong co Internet:' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        # print("off - 3")
        for i in range(1, max_Relay + 1):
            if(DB.check_syn("controller", i)==False): # phat hien ra la co data chua sync- vet tu day
                DB.update_data_row("controller", i, "ok")
                # data = DB.get_data_row("controller", i)
            else:
                pass
        
        Windowns.backup_Synchronous(2)
        # print("off - 4")
        # đã đồng bộ xong - quay về cờ ban đầu, tiếp tục vòng
        CONSTANT.flag_backup = 0
        CONSTANT.flag_backup_N = 1  

        # cho phép truy xuất dữ liệu
        CONSTANT.Flag_Update_Syn_Data = False
        # Cho phép bấm relay
        CONSTANT.Flag_Update_Syn_Button = False

        CONSTANT.Flag_Update_GUI  = False

        logging.debug('ket thuc dong bo Synchronous  : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    except:
        logging.debug('Synchronous error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))   

def Backup():
    try:
        Windowns.backup_Synchronous(0)

        DB.creat_table("nongtrai_G00")
        DB.creat_table("nongtrai_G01")
        DB.creat_table("controller")
        # print("backup begin")

        # 2 cờ này báo xảy ra quá trình backup
        CONSTANT.flag_backup = 1
        CONSTANT.flag_backup_N = 0  
        CONSTANT.Flag_Update_Syn_Data == False # mất mạng thì vẫn cho phép lấy dữ liệu

        logging.debug('Bat dau Backup Data  : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    except:
        logging.debug('Backup error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))   

class YouThread(QtCore.QThread): # inheritance
    global client

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    # 0 - 1 : start
    # 0 - 0 : running
    # 1 - 1 : pass
    # 1 - 0 : có vết backup
    def run(self): #  background task - chạy ngầm để gửu dữ liệu : this is non-daemon thread. if use daemon : either complete or killed when main thread exits.
        while(True): # note daemon sử dụng khi : you don’t mind if it doesn’t complete or left in between.
            try: 
                if(check_internet() == False): # khi mat mang se backup
                    time.sleep(1) # delay 1 day - loai bo truong hop mang khong on dinh
                    if(check_internet() == False):
                        if((CONSTANT.flag_backup == 0) and (CONSTANT.flag_backup_N == 1)): # danh dau khi mat mang
                            #logging.debug(str(flag_backup) + str(flag_backup_N)+ '    ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                            Windowns.display_internet(0)
                            Backup()
                        else:
                            pass          
                else:   
                    # khi có mạng sẽ đẩy lên server
                    # message backup -  CONSTANT.DATAG00 or  CONSTANT.DATAG00
                    if((CONSTANT.flag_backup == 1) and (CONSTANT.flag_backup_N == 0)):
                        Windowns.display_internet(1)
                        Synchronous()
                    else:
                        pass
            except:
                logging.debug('YouThread error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  
        time.sleep(1) # delay 1 day 

thread = YouThread() 
thread.start()

def Init_Thread():
    try:
        #---data---------------------------------------------------------------------------------------------
        CONSTANT.Thread_GW.timeout.connect(Thread_GatewayBlue_QT)
        CONSTANT.Thread_GW.start(120000)

        # muốn đồng bộ nhanh - 2  thread  phải lệch khe thời gian
        CONSTANT.Thread_GUI.timeout.connect(Thread_UpdateGUI_QT)
        CONSTANT.Thread_GUI.start(125000)

        #-----------------------------------------------------------------------------------------------------


        # 10s gọi hàm này kiểm tra đk SM một lần
        CONSTANT.Thread_pump1.timeout.connect(Thread_pump1)
        CONSTANT.Thread_pump1.start(121000)
        CONSTANT.SubThread_pump1.timeout.connect(Windowns.countdown_pump1)

        # 10s gọi hàm này kiểm tra đk Light một lần
        CONSTANT.Thread_curtain1.timeout.connect(Thread_curtain1)
        CONSTANT.Thread_curtain1.start(121000)
        CONSTANT.SubThread_curtain1.timeout.connect(Windowns.countdown_curtain1)
        
        #-----------------------------------------------------------------------------------------------------   
    except:
        logging.debug('Init_Thread error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

def DeInit_Thread():
    try:
        CONSTANT.Thread_GW.stop()
        CONSTANT.Thread_GUI.stop()

        CONSTANT.Thread_pump1.stop()
        CONSTANT.Thread_curtain1.stop()
    except:
        logging.debug('DeInit_Thread error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

#---end------------------------------------------------------------------------------------------------


def Init_api():
    try:
        with open('api\\config.json') as f: 
            account = json.load(f)

        response = requests.post("https://smartfarm.tinasoft.com.vn/api/v1/auth", data=account)
        login    = response.json()

        headers = {
            "Authorization":"Bearer "+login["auth_token"],
            "Accept":"/",
            "Cache-Control":"no-cache",
            "Connection": "keep-alive",
        }
        try:
            response_get = requests.get("https://smartfarm.tinasoft.com.vn/api/v1/information",headers=headers)
            response_get = response_get.json()
        except:
            return False

        # G00
        CONSTANT.L['min'] = response_get[0]["stage"]["min_light"]
        CONSTANT.L['max'] = response_get[0]["stage"]["max_light"]
        CONSTANT.PH['min'] = response_get[0]["stage"]["min_PH"]
        CONSTANT.PH['max'] = response_get[0]["stage"]["max_PH"]
        CONSTANT.T['min'] = response_get[0]["stage"]["min_temp"]
        CONSTANT.T['max'] = response_get[0]["stage"]["max_temp"]
        CONSTANT.H['min'] = response_get[0]["stage"]["min_hum"]
        CONSTANT.SM['min'] = response_get[0]["stage"]["min_soil_moisture"]
        CONSTANT.SM['max'] = response_get[0]["stage"]["max_soil_moisture"]

        #update GUI
        Windowns.app.tab1_T_min.setText(str(CONSTANT.T['min']))
        Windowns.app.tab1_T_max.setText(str(CONSTANT.T['max']))

        Windowns.app.tab1_L_min.setText(str(CONSTANT.L['min']))
        Windowns.app.tab1_L_max.setText(str(CONSTANT.L['max']))

        Windowns.app.tab1_H_min.setText(str(CONSTANT.H['min']))
        Windowns.app.tab1_H_max.setText(str(CONSTANT.H['max']))

        Windowns.app.tab1_PH_min.setText(str(CONSTANT.PH['min']))
        Windowns.app.tab1_PH_max.setText(str(CONSTANT.PH['max']))

        if(response_get[0]["stage"]["name"]=="germination stage"):
            Windowns.app.tab1_stage.setText("Cây con")
        elif(response_get[0]["stage"]["name"]=="development stage"):
            Windowns.app.tab1_stage.setText("Cây trưởng thành")
        elif(response_get[0]["stage"]["name"]=="harvest stage"):
            Windowns.app.tab1_stage.setText("Thu hoạch")
        else:
            pass

        if(response_get[0]["seed_name"]=="tomato"):
            Windowns.app.label.setText("VƯỜN CÀ CHUA")
            Windowns.app.label_48.setText("CÀ CHUA")
            Windowns.app.label_50.setText("Hạt giống: Cà Chua")
        elif(response_get[0]["seed_name"]=="pakchoi"):
            Windowns.app.label.setText("VƯỜN CẢI CHÍP")
            Windowns.app.label_48.setText("CẢI CHÍP")
            Windowns.app.label_50.setText("Hạt giống: Cải Chíp")
        elif(response_get[0]["seed_name"]=="brassica"):
            Windowns.app.label.setText("VƯỜN CẢI NGỌT")
            Windowns.app.label_48.setText("CẢI NGỌT")
            Windowns.app.label_50.setText("Hạt giống: Cải Ngọt")
        elif(response_get[0]["seed_name"]=="cucumber"):
            Windowns.app.label.setText("VƯỜN DƯA CHUỘT")
            Windowns.app.label_48.setText("Dưa Chuột")
            Windowns.app.label_50.setText("Hạt giống: Dưa Chuột")
        elif(response_get[0]["seed_name"]=="cabbage"):
            Windowns.app.label.setText("VƯỜN BẮP CẢI")
            Windowns.app.label_48.setText("Bắp Cải")
            Windowns.app.label_50.setText("Hạt giống: Bắp Cải")
        else:
            pass
    except:
        logging.debug('Init_api error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

if __name__ == "__main__": # điểm bắt đầu của một chương trình


    Init_api()
    requirePort()
    Init_UI()
    Init_Button()
    Init_mqtt()
    Init_Thread()

    Windowns.app.show()
    sys.exit(Windowns.App.exec())
