# Serial
import minimalmodbus
import serial
import serial.tools.list_ports

# library programer development
import constant as CONSTANT
import math, logging
import time

from datetime import datetime

logging.basicConfig(filename='logs\\error_code.log', level=logging.DEBUG)

'''
    đọc dữ liệu từ gateway(Xanh) : sử dụng thư viện minimalmodbus
'''

class Gateway():
    # init MOSBUS RTU
    def __init__(self, port_name, id_device=1):
        try:
            self.instrument = minimalmodbus.Instrument(port_name, id_device) 
            self.instrument.serial.baudrate = 9600
            self.instrument.serial.timeout = 0.05
            self.instrument.mode = minimalmodbus.MODE_RTU  # seconds
            self.initialize()
        except:
            logging.debug('Gateway, __init__ : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def initialize(self): # khi mình khởi động tắt tất cả thiết bị và cập nhập trạng thái off trên app
        try:
            # for i in range(27, 31):
                # self.control_RL(i, 1, 0)
            self.control_RL(23, 1, 0)
            pass
        except:
            logging.debug('Gateway, initialize : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


    # convert data to int 16
    def convert_data(self, data):
        try:
            value = ''
            for i in range(0, len(data)):
                value += hex(data[i])
            value = value.replace('0x', '')
            value = '0x'+value
            return int(value, 16)
        except:
            logging.debug('Gateway, convert_data : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    # registeraddress- Search in file Modbus memmap of WR433 V1.9 : C:\Users\Pham Van Phuc\Desktop\SFARM-master
    # get number of node of Wriless 
    def get_num_of_node(self):
        try :
            data = self.instrument.read_registers(
                registeraddress=272, number_of_registers=2, functioncode=3)
            value = self.convert_data(data)
            return value
        except:
            logging.debug('Gateway, Get_num_of_node : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return 0

    # read mosbus adr
    def get_modbus_adr(self):
        try:
            data = self.instrument.read_registers(
                registeraddress=256, number_of_registers=1, functioncode=3)
            value = self.convert_data(data)
            return value
        except:
            logging.debug('Gateway, Get_modbus_adr : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return 0

    # read mosbus baudrate
    def get_modbus_baudrate(self):
        try:
            data = self.instrument.read_registers(
                registeraddress=257, number_of_registers=1, functioncode=3)
            value = self.convert_data(data)
            return value
        except:
            logging.debug('Gateway, Get_modbus_baudrate : error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return 0

    # read mosbus parity
    def get_modbus_parity(self):
        try:
            data = self.instrument.read_registers(
                registeraddress=258, number_of_registers=1, functioncode=3)
            value = self.convert_data(data)
            return value
        except:
            logging.debug('Gateway, Get_modbus_parity  error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return 0
# end file - Modbus memmap of WR433 V1.9

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------


# get id of node - do họ đặt
    ''' 
        ID  : Kinds of sensors
        1   : SOIL MOISTURE
        2   : HUMIDITY
        3   : LIGHT
        4   : RELAY
        pos : thứ tự các node mình setup
    '''
    def get_node_id(self, pos=1, id=1):        # Read ID of device  !! OK check xong
        try:
            data = self.instrument.read_registers(
                    registeraddress=(271 + (pos)*2), number_of_registers=2, functioncode=3)
            value = self.convert_data(data)
            return str(value)
        except:
            logging.debug('Gateway, Get_node_id : ' + str(pos) + ' error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return 0


# registeraddress : Template_WR433_V1.6:SFARM-master\Daviteq Modbus Configuration Tool Version 1.2
    # get main parmeter
    ''' 
        ID  : Kinds of sensors
        1   : SOIL MOISTURE
        2   : HUMIDITY
        3   : LIGHT
        4   : RELAY
    '''
    def get_main_parameter(self, pos, id):  # read Data   !! OK check xong
        if(id == 1):
            try:
                data = self.instrument.read_registers(registeraddress=(41217 + (pos-1)*256 + int((pos-1)/10)*1536), 
                number_of_registers=1, functioncode=3)  
                return round((data[0]/10), 2)
            except:
                logging.debug('Gateway, Get_main_parameter : ' + str(pos) + ' error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                return 0
        elif(id == 2):
            try:
                data = self.instrument.read_float(registeraddress=(41217 + (pos-1)*256 + int((pos-1)/10)*1536), 
                number_of_registers=2, functioncode=3)
                return round(data, 2)
            except:
                logging.debug('Gateway, Get_main_parameter : ' + str(pos) + ' error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                return 0
        elif(id == 3):
            try:
                data = self.instrument.read_float(registeraddress=(41217 + (pos-1)*256 + int((pos-1)/10)*1536), 
                number_of_registers=2, functioncode=3)
                return round(data, 2)
            except:
                logging.debug('Gateway, Get_main_parameter : ' + str(pos) + ' error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                return 0
        else:
            pass
        time.sleep(0.5)


# address in file memap of WS433-RL - C:\Users\Pham Van Phuc\Desktop\SFARM-master
    ''' 
        ID  : Kinds of sensors
        1   : SOIL MOISTURE
        2   : HUMIDITY
        3   : LIGHT
        4   : RELAY
    '''
    def get_second_parameter(self, pos=1, id=1):     # get second parameter     !! OK check xong
        try:
            data = self.instrument.read_float(registeraddress=(41220 + ((pos-1)*256)), number_of_registers=2, functioncode=3)
            return round(data, 2)
        except:

            logging.debug('Gateway, Get_second_parameter : ' + str(pos) + ' error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return 0            
    
    ''' 
        ID  : Kinds of sensors
        1   : SOIL MOISTURE
        2   : HUMIDITY
        3   : LIGHT
        4   : RELAY
    '''
    def get_battery(self, pos=1, id=1):       # get Batterry    !! OK check xong
        try:
            data = self.instrument.read_register(41216 + ((pos-1)*256)+ + int((pos-1)/10)*1536)
            return data      
        except:
            logging.debug('Gateway, Get_battery : ' + str(pos) + ' error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return 0
        time.sleep(0.5)



    ''' 
        ID  : Kinds of sensors
        1   : SOIL MOISTURE
        2   : HUMIDITY
        3   : LIGHT
        4   : RELAY
    '''
    def get_status_node(self, pos=1, id=1):     #kiểm tra xem node là node gì VD : 11 - độ ẩm đất  !! OK check xong
        try:
            data = self.instrument.read_register((41219 + (pos-1)*256))
            return CONSTANT.STATUS_NODE[str(data)]
        except:
            logging.debug('Gateway, Get_Status_node : ' + str(pos) + ' error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return 0
        time.sleep(0.5)

    ''' 
        ID  : Kinds of sensors
        1   : SOIL MOISTURE
        2   : HUMIDITY
        3   : LIGHT
        4   : RELAY
    '''
    # 68 : node1,2    69 : node3,4 ...
    def get_RFsignal(self, pos=1, id=1):     # get RF signal            !! OK check xong
        try: 
            data = self.instrument.read_registers(registeraddress=(67 + math.ceil(pos/2)), number_of_registers=1, functioncode=3)
            data = hex(data[0]).replace('0x', '')
            hi_byte = data[0]
            lo_byte = data[len(data) - 1]

            if ((pos%2) != 0): # 1,3,5,7,9 ... hi_byte
                return CONSTANT.RSSI[str(hi_byte)]
            else:
                return CONSTANT.RSSI[str(lo_byte)]
        except:
            logging.debug('Gateway, get_RFsignal : ' + str(pos) + ' error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return 0
        time.sleep(0.5)


    def get_Temperature(self, pos=1, id=1):
        try:
            data = self.instrument.read_float((41219 + (pos-1)*256 + 1), number_of_registers=2, functioncode=3)
            return round(data, 2)
        except:
            logging.debug('Gateway, get_Temperature : ' + str(pos) + ' error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return 0
        time.sleep(0.5)

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

    '''
        5 RELAY -  1 RELAY 2 chanel
        pos : vị trí của NODE RELAY trên hệ thống: thứ tự mình add vào trong gateway
        chanel : chanel 1, 2
        status : 1 - ON ,0 - OFF 
    '''
#test realy--------------------------------------------------------------------------------------------
    #   pos : thứ tự relay trong gateway
    #   chanel : từng chân relay trong module relay
    def control_RL(self, pos, chanel, status): # control realy
        try:
            self.instrument.write_register(registeraddress=(2000 + (pos-1)*8 +(chanel-1)), value=status,
                                                number_of_decimals=0, functioncode=16, signed=False)

        except:
            logging.debug('Gateway, control_RL : ' + str(pos) + ' error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            pass
    
    # get status of relay - phản hồi trạng thái hiện tại của relay
    def get_status_RL(self, pos, chanel):
        try:
            data = self.instrument.read_registers(
                    registeraddress=(2000 + (pos-1)*8 +(chanel-1)), number_of_registers=1, functioncode=3)
            return data[0]
        except:
            logging.debug('Gateway, get_status_RL : ' + str(pos) + ' error ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            pass


#---------------------------------------------------------------------------------------------------------