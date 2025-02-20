import time
import threading
import pandas as pd

from PowerSensor import PowerSensor
from SignalOrig import Sg


class Device:

    def __init__(self):
        self._sg = Sg()
        self._ps = PowerSensor()
        self._one_list = list()
        self._all_list = list()
        # THREAD
        self._thread = threading.Thread(target=self._working, daemon=True)
        self._thread.start()

    def _working(self):
        while 1:
            if self._sg.is_link() and self._ps.get_online():
                ena = self._sg.get_power_ena()
                if ena:
                    power = self._ps.get_power()
                    print(f"power={power}")
                # else:
                #     self._sg.send_udp_freq_stop_cmd(0)
                time.sleep(0.01)
            else:
                time.sleep(1)

    def test_func1(self):
        tx_power = -10
        freq = 1e9
        ts = time.time()
        for i in range(10):
            freq += 10000000
            self._sg.send_visa_freq_cmd(freq=freq)
            # self._ps.set_freq(freq=freq)
            for j in range(20):
                self._one_list = list()
                self._sg.send_visa_pow_cmd(power=tx_power)
                time.sleep(0.08)
                power = self._ps.get_power()
                self._one_list.append(freq)
                self._one_list.append(tx_power)
                self._one_list.append(power)
                self._all_list.append(self._one_list)
                print(f"freq={freq}, power={tx_power}, rx_power={power}")
                tx_power += 1
                if tx_power > 10:
                    tx_power = -10
        print(time.time() - ts)
        pf = pd.DataFrame(self._all_list, columns=["FREQ", "POWER", "RX_POWER"])
        pf.to_csv("2.csv", header=True, sep=',', index=False)

    def test_func_trigger(self):
        self._sg.set_freq_start(freq=600)
        self._sg.set_freq_stop(freq=600)
        self._sg.set_freq_step(10)
        self._sg.set_thread_start()  # 发送频点数据
        time.sleep(0.01)
        self._sg.send_udp_cal_start()  # 设置开始读取寄存器

    def connect_device(self):
        self._sg.set_sg_link(True, "192.9.16.1")
        self._ps.set_online()
        self._ps.set_dev_name(name=self._ps._list_name[0])
        self._ps.connect_ps()


if __name__ == '__main__':
    device = Device()
    device.connect_device()
    device.test_func_trigger()
    # device.test_func()
    while 1:
        time.sleep(1)

'''
set freq=1000000000.0 power=-9, ps_rx_power=-9.84139114
set freq=1010000000.0 power=-8, ps_rx_power=-8.89633378
set freq=1020000000.0 power=-7, ps_rx_power=-8.0087655
set freq=1030000000.0 power=-6, ps_rx_power=-7.01279561
set freq=1040000000.0 power=-5, ps_rx_power=-6.02850616
set freq=1050000000.0 power=-4, ps_rx_power=-5.05053412
set freq=1060000000.0 power=-3, ps_rx_power=-4.0688168
set freq=1070000000.0 power=-2, ps_rx_power=-3.12612215
set freq=1080000000.0 power=-1, ps_rx_power=-2.16274013
set freq=1090000000.0 power=0, ps_rx_power=-1.22149932
'''