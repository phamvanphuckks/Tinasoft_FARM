RSSI = {
    "4": "Good",
    "3": "Good",
    "2": "Medium",
    "1": "Bad",
    "0": "NULL"
}

def get_RFsignal(pos=1, id=1):     # get RF signal            !! OK check xong
    try: 
        a = [1028]  # 00 04
        low_byte  = a[0] & 255
        high_byte = (a[0]>>8) & 255

        print
        if ((pos%2) != 0): #(odd) 1,3,5,7,9 ... hi_byte
            return RSSI[str(high_byte)]
        else:
            return RSSI[str(low_byte)]
    except:
        return 0



print(get_RFsignal(23, 4))
print(get_RFsignal(24, 4))