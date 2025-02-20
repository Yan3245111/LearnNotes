import time

import pandas as pd

from Fs import Fs
from Sg import Sg

SG_IP = "192.9.16.1"
PS_IP = "192.168.1.20"


"""
测试一：fft模式，读取的时候打开持续扫描，读取完毕设置单次扫描
测试记录1：100ms切频点有问题，连续几个点功率不变，中间有的频点功率值也不对
测试记录2：150ms同上
测试记录3：200ms同上 
结论：那就不是延时的问题

写着最小fft是10ns扫描，但是不加延时读取数据不对
切频点不加延时，读取之前加延时，关闭屏幕显示，30ms延时读取，切频点后前三个功率不对，200ms在测试中 第一个点不对

测试2：前5个点500ms延时，后面100ms延时，单次扫描设置，第一个点功率为8，数据不对
测试3：400ms + 120ms 有错误数据
测试4：peak search 连续追踪最大值，关掉试一下，扫描设置成1ms，span设置为100Khz  vbw 1khz rbw 1khz ref 20dBm，
    说数据可以用-80开始有不对的值, 切频点的时候有不对的地方
测试5：切频点的时候用wait指令读取，其它点用正常读取
"""


class Devices:

    def __init__(self):
        self._sg = Sg()
        self._fs = Fs()
        self._df = list()

    def connect_device(self):
        self._sg.set_sg_link(link_ena=True, ip_str=SG_IP)
        self._fs.set_visa_link(link_ena=True, ip_str=PS_IP)
        # self._fs.set_fft_high()

    def read_data(self):
        all_line = list()
        self._df = pd.read_csv("test_3U遍历表100M20G - 副本.csv")
        self._fs.set_fft()
        self._fs.set_sweep_once(True)
        ts = time.time()
        c = 0
        for i in range(len(self._df)):
            # time_delay = 0.3 if c <= 5 else 0.05
            sg_freq = self._df['W_RFFreq'][i]
            rf_att = self._df['W_RFAtt'][i]
            if_att = self._df['W_IFAtt'][i]
            num_att = self._df['W_NumIFAtt'][i]
            fs_freq = self._df['W_KsCenterFreq'][i]
            fs_ref = self._df['W_KsRefLevel'][i]
            # print(sg_freq, rf_att, if_att, num_att, fs_freq, fs_ref)
            if fs_ref != self._fs.get_ref() or fs_freq * 1000000 != self._fs.get_freq():
                self._sg.send_udp_freq_cmd(sg_freq)
                c = 0
                # self._fs.set_sweep_once(True)
                # time.sleep(0.5)
                # self._fs.set_sweep_once(False)
                self._fs.send_freq_cmd(freq_hz=fs_freq * 1000000)
                self._fs.send_rel_cmd(ref=fs_ref)
            time_delay = 1 if c == 0 else 0.08
            self._sg.send_udp_rf_att_cmd(rf_att)
            self._sg.send_udp_if_att_cmd(if_att)
            self._sg.send_udp_if_digital_att_cmd(num_att)
            # self._fs.set_sweep_once(ena=False)
            time.sleep(time_delay)
            if c == 0:
                p_freq, p_power = self._fs.read_peak_point_wait()
                # print(1)
            else:
                # time.sleep(time_delay)
                p_freq, p_power = self._fs.read_peak_point()
            # self._fs.set_sweep_once(ena=True)
            one_line = [sg_freq, rf_att, if_att, num_att, p_power]
            all_line.append(one_line)
            print(f'read freq={p_freq}, power={p_power}')
            c += 1
            if p_freq == 0 and p_power == 0:
                print(f"校准结束，时间：={time.time() - ts}")
                break
        df = pd.DataFrame(all_line)
        df.to_csv("res80_5.csv", header=["fs_freq", "rf_att", "if_att", "num_att", "fs_power"], index=False, sep=",")
        print(f"保存文件成功， ts={time.time() - ts}")


if __name__ == '__main__':
    device = Devices()
    device.connect_device()
    device.read_data()
    while 1:
        time.sleep(1)
