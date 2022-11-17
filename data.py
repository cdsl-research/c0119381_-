from machine import I2C,Pin
from vl53l1x import VL53L1X
import time

""" パラメータ """
# i2c関係
I2C_SCL_PIN = 22
I2C_SDA_PIN = 21

# XSHUTに接続するPin番号
x_suht_pin = [0,4,16]
""" パラメータ(終わり) """

class VL53L1X_S():
    # 複数の距離センサを取り扱うクラス

    def __init__(self, i2c, x_suht_pin):
        self.vl53l1x_s = []
        self.pin_s = []

        # Pinの初期化
        for pin_no in x_suht_pin:
            self.pin_s.append(Pin(pin_no, Pin.OUT))
            self.pin_s[-1].value(0)
    
        # 各センサの初期化(アドレス変更)
        for i in range(len(x_suht_pin)):
            time.sleep(0.2)
            self.pin_s[i].value(1)
            self.vl53l1x_s.append(VL53L1X(i2c))
            self.vl53l1x_s[-1].writeReg(0x0001, 64+i & 0x7F)
            self.vl53l1x_s[-1].address = 64 + i
            print("vl53l1x addr:%d distance:%dmm" % (64 + i , self.vl53l1x_s[-1].read()))
        
    def read_sensors(self):
        # データを配列で返却(3台の場合100msで返却)
        out = []
        for vl53l1x in self.vl53l1x_s:
            time.sleep(0.03)
            out.append(vl53l1x.read())
        time.sleep(0.01)
        return out
        
    
if __name__ == '__main__':
    i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))
    vl53l1x = VL53L1X_S(i2c,x_suht_pin)


while True:
    data = vl53l1x.read_sensors()
    print("%d,%d,%d" % (data[0],data[1],data[2]))