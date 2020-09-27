from PyQt5.QtCore import QTimer, QTime, QThread, Qt

#api
global auth_token

# thread 
global Thread_GUI, Thread_GW, Thread_DB
Thread_GUI = QTimer()
Thread_GW  = QTimer()
Thread_DB  = QTimer()

global Check_Internet
Check_Internet = QTimer()

#--------------------------------------------------------------------------------------------------

global DATA_G00, DATA_G01, DATA_G02


DATA_G00 = {
    "sub_id": "G00",
    "time"  : "",
    "NODE1":  {"node": 1,"name": "soil_moistrure1", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE2":  {"node": 2,"name": "soil_moistrure2", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE3":  {"node": 3,"name": "soil_moistrure3", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE4":  {"node": 4,"name": "soil_moistrure4", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE5":  {"node": 5,"name": "soil_moistrure5", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE6":  {"node": 6,"name": "soil_moistrure6", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE7":  {"node": 7,"name": "soil_moistrure7", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE8":  {"node": 8,"name": "soil_moistrure8", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE9":  {"node": 9,"name": "soil_moistrure9", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE10": {"node": 10,"name": "soil_moistrure10", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},

    "NODE21": {"node": 21,"name": "humidity1",         "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE23": {"node": 23,"name": "light1",            "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE25": {"node": 25,"name": "temperature1",      "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"}
}

DATA_G01 = {
    "sub_id":"G01",    
    "time"  : "",
    "NODE11": {"node": 11,"name": "soil_moistrure11", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE12": {"node": 12,"name": "soil_moistrure12", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE13": {"node": 13,"name": "soil_moistrure13", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE14": {"node": 14,"name": "soil_moistrure14", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE15": {"node": 15,"name": "soil_moistrure15", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE16": {"node": 16,"name": "soil_moistrure16", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE17": {"node": 17,"name": "soil_moistrure17", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE18": {"node": 18,"name": "soil_moistrure18", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE19": {"node": 19,"name": "soil_moistrure19", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE20": {"node": 20,"name": "soil_moistrure20", "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},

    "NODE22": {"node": 22,"name": "humidity2",         "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE24": {"node": 24,"name": "light2",            "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"},
    "NODE26": {"node": 26,"name": "temperature2",      "id": 0, "value" : 0, "battery" : 0, "RF_signal":"", "time":"", "syn":"error"}
}


DATA_RELAY = {
    "sub_id": "G02",
    "time"  :  "",
    "NODE27": {"node": 27,"name": "relay1", "id":0,  "value" : 0, "battery": 100, "RF_signal":"NULL", "time":"", "syn":"error"},
    "NODE28": {"node": 28,"name": "relay2", "id":0,  "value" : 0, "battery": 100, "RF_signal":"NULL", "time":"", "syn":"error"},
    "NODE29": {"node": 29,"name": "relay1", "id":0,  "value" : 0, "battery": 100, "RF_signal":"NULL", "time":"", "syn":"error"},
    "NODE30": {"node": 30,"name": "relay2", "id":0,  "value" : 0, "battery": 100, "RF_signal":"NULL", "time":"", "syn":"error"},
    "NODE31": {"node": 31,"name": "relay5", "id":0,  "value" : 0, "battery": 100, "RF_signal":"NULL", "time":"", "syn":"error"}
}

#------------------------------------------------------------------------------------------------------------------------------------

global SENSOR, RSSI

SENSOR = {
    "soil_moistrure" : 1,
    "humidity"       : 2,
    "light"          : 3,
    "relay"          : 4
}

RSSI = {
    "4": "Good",
    "3": "Good",
    "2": "Medium",
    "1": "Bad",
    "0": "NULL"
}

global T, H, SM

L = {
    'min': 2000,
    'max': 2300
}

T = {
    'min': 15,
    'max': 30
}
H = {
    'min': 85,
    'max': 95
}

SM = {
    'min': 12,
    'max': 17
} 

global flag_pump, flag_curtain
flag_pump = 0
flag_curtain = 0

global GW_Blue_NAME

# name GW default - tên này có thể thay đổi nếu port thay đổi
GW_Blue_NAME  = "COM3"        # GateWay(Xanh) : thu dữ liệu của bọn đại việt và điều khiển máy bơm

