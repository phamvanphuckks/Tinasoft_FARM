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

import logging, threading

# define globale
Windowns = qt5Class()
DB       = SQLite.DataBase()

'''
---------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------
'''

logging.basicConfig(filename='logs\\error_code.log',level=logging.INFO)

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
                logging.info('Khoi tao Mqtt error - mqtt error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))                
        else:
            logging.info('Khoi tao Mqtt error - khong co internet: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    except:
        logging.info('Init_mqtt error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

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
        if (device == 1):  # pump1
            if(status == 1):
                GW_Blue.control_RL(23, 1, 1) # GateWay(Xanh) điểu khiển Relay 
                if(get_status(27) == "1"):
                    Windowns.UpdatePicture(device, status) # thay đổi trên app  
            elif(status == 0):
                GW_Blue.control_RL(23, 1, 0)
                if(get_status(27) == "0"):
                    Windowns.UpdatePicture(device, status)
            else:
                pass
        elif(device == 2): # curtain1
            if(status == 1):
                GW_Blue.control_RL(24, 1, 1) # GateWay(Xanh) điểu khiển Relay 
                if(get_status(28) == "1"):
                    Windowns.UpdatePicture(device, status) # thay đổi trên app
            elif(status == 0):
                GW_Blue.control_RL(24, 1, 0)
                if(get_status(28) == "0"):
                    Windowns.UpdatePicture(device, status)
            else:
                pass
        else:
            pass
    except:
        logging.info('ControlDevice error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

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
                logging.info('Loi Publish get_status_all - mqtt error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            logging.info('Loi Publish get_status_all - Khong co Internet : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    except:
        logging.info('get_status_all error : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

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
                logging.info('Loi publish get_status - mqtt error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))        

        else:
            DB.insert_data_row("controller", pos, CONSTANT.DATA_RELAY["NODE" + str(pos)]["name"],CONSTANT.DATA_RELAY["NODE" + str(pos)]["id"],
            CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"], CONSTANT.DATA_RELAY["NODE" + str(pos)]["RF_signal"], 100, 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "error")

            logging.info('khong co Internet, get_status ghi vao Database : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        return CONSTANT.DATA_RELAY["NODE" + str(pos)]["value"]
    except:
        logging.info('get_status error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))   

def on_connect(client, userdata, flags, rc):    # subscrie on  topic
    # print("Connected with result code " + str(rc))
    try:
        client.subscribe(MQTT_TOPIC_CONTROL)
    except:
        logging.info('subscribe topic error : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

def on_message(client, userdata, msg):  # received data - chua code xong
    # print(msg.topic+" "+str(msg.payload))
    try:
        data = json.loads(msg.payload.decode('utf-8'))
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
    except:
        logging.info('Loi on_message : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))          


def Init_Button():
    try:
        Windowns.app.tab2_btn_r1off.clicked.connect(lambda:ControlDevice(1, 0))
        Windowns.app.tab2_btn_r1on.clicked.connect(lambda:ControlDevice(1, 1))

        Windowns.app.tab2_btn_r2off.clicked.connect(lambda:ControlDevice(2, 0))
        Windowns.app.tab2_btn_r2on.clicked.connect(lambda:ControlDevice(2, 1))

    except:
        logging.info('Init_Button Error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))   

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
            logging.info('Khoi tao UI error : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            sys.exit()
    else:
        QMessageBox.critical(Windowns.app, "LỖI KẾT NỐI",
                                  "KHÔNG CÓ COM NÀO ĐƯỢC KẾT NỐI")
        logging.info('Khoi tao UI error : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
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
        logging.info('requirePort error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))   

#---end-----------------------------------------------------------------------------------------------------------


def Thread_GatewayBlue():
    global GW_Blue, client
    try:
        logging.info('Lay Data tu sensor Chu ky 120s : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

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
                logging.info('Thread_GatewayBlue: Loi publish data G00, G01  - mqtt error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            try:
                DB.insert_data_nongtraiG01("nongtrai_G01", "error") 
                DB.insert_data_nongtraiG00("nongtrai_G00", "error") 
            except:
                logging.info('Thread_GatewayBlue: Loi publish data G00, G01  - khong co Internet : ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    except:
        logging.info('Thread_GatewayBlue error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))   

def Thread_GatewayBlue_QT():
    try:
        Thread_GW  = threading.Thread(target=Thread_GatewayBlue, args=())
        Thread_GW.setDaemon(True)

        Thread_GW.start()
    except:
        logging.info('Thread_GatewayBlue_QT error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

def Thread_UpdateGUI_QT():
    global Windowns
    try:
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

        Windowns.Update_RF_Relay(CONSTANT.DATA_RELAY)
        # CONSTANT.Flag_Update_GUI  = False
    except:
        logging.info('Thread_UpdateGUI_QT error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  
  

class YouThread(QtCore.QThread): # inheritance
    global client

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    def run(self): 
        while(True):
            try: 
                if(check_internet() == False): # khi mat mang se backup
                    time.sleep(1) # delay 1 day - loai bo truong hop mang khong on dinh
                    if(check_internet() == False):
                        Windowns.display_internet(0)
                else:   
                        Windowns.display_internet(1)
            except:
                logging.info('YouThread error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  
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
    except:
        logging.info('Init_Thread error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

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
        logging.info('Init_api error: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  

if __name__ == "__main__": 

    Init_api()
    requirePort()
    Init_UI()
    Init_Button()
    Init_mqtt()
    Init_Thread()

    Windowns.app.show()
    sys.exit(Windowns.App.exec())
