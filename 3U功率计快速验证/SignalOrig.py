import time
import struct
import socket

import numpy
import pyvisa
from typing import Optional
from threading import Thread

PKG_HEAD = b'\x55\xaa\xaa\x55\xff\xff\xff\xff'
PKG_TAIL = b'\xaa\x55\x55\xaa\xff\xff\xff\xff'
UDP_PORT = 20481
VISA_PORT = 5025

# HEAD
UDP_HEAD = b'\xab\xab\xba\xba'
CMD_UDP_HEAD = b'\x7e\x7e'
# W OR R
UDP_WRITE = b'\x01'
# FUNC
UDP_FUNC_CONNECT = b'\x01'
UDP_FUNC_RF_FREQ = b'\x03'
UDP_FUNC_RF_ATT = b'\x04'
UDP_FUNC_IF_ATT = b'\x05'
UDP_FUNC_IF_DIGITAL_ATT = b'\x06'
UDP_FUNC_RF_ENA = b'\x07'
UDP_FUNC_PL_ADDR = b'\x08'
UDP_FUNC_PL_DATA = b'\x09'

UDP_FUNC_SET_FREQ_STOP = b'\x11'
UDP_FUNC_SET_CAL_START = b'\x16'
# END
UDP_END = b'\xe7\xe7'


class Sg:

    def __init__(self):
        self._target_addr = None  # type:tuple
        self._udp_client = None
        self._visa_device = None
        self._pow = float()
        self._freq = float()
        self._ena = False
        self._is_link = False
        self._start_freq = float()
        self._stop_freq = float()
        self._step_freq = float()
        self._power_ena = 0
        # THREAD
        self._thread = None
        self._udp_thread = Thread(target=self._udp_recv, daemon=True)
        self._udp_thread.start()

    def _udp_recv(self):
        while 1:
            try:
                if self._udp_client is not None:
                    data, peer = self._udp_client.recvfrom(20)
                    print(data)
                    # ena = data << 32
                    # print(ena)
                    # self._power_ena = ena
            except socket.error as err:
                pass

    def get_power_ena(self) -> int:
        return self._power_ena

    @staticmethod
    def change_bytes_with_4(data: bytes) -> bytes:
        group_count = int(len(data) / 32)
        res_data = bytes()
        for i in range(group_count):
            num = 8
            one_group = data[i * 32: (i + 1) * 32]
            for j in range(8):
                res_data += one_group[(num - 1) * 4: num * 4]
                num -= 1
        return res_data

    '''
    head = 0x55aaaa55ffffffff
    cmd = 3(4B)
    remain = 0(52B)
    data1 = 0x0000 + freq(2B) + 射频(2B) + 中频(2B)
    data2 = 
    ......
    tail 0xaa5555aaffffffff
    remain = 0(56B)
    freq_num 必须是8的整数倍，不够的话多几条0
     */
    // power sensor FREQ: unit: MHz 射频衰减 she_att 0-480 中频 mid_att 7，频率步进10M，功率步进1dbm 先发包头，然后发数据，然后发包尾，
      数据位如果不是8的倍数要补0
    每8个4字节，要调转一下顺序 
    ps最多只能接收2048个字节
    '''
    def _working(self):
        count = int((self._stop_freq - self._start_freq) / self._step_freq) + 1
        remain_count = int(numpy.ceil(count * 121 / 8) * 8 - count * 121)
        print(f'start freq={self._start_freq} stop freq ={self._stop_freq} step freq={self._step_freq}, count={count}, remian={remain_count}')
        one_freq = 0
        rx_data = bytes()
        rx_head = PKG_HEAD + struct.pack("i", 3) + struct.pack('H', 0) * 26
        print(rx_head)
        rx_tail = PKG_TAIL + struct.pack('H', 0) * 28
        rx_head = self.change_bytes_with_4(data=rx_head)
        print(f"rx_head={rx_head}")
        self.send_udp_freq_cail_data(data=rx_head)
        for i in range(count):
            if i == count - 1 and one_freq < self._stop_freq:
                one_freq = self._stop_freq
            else:
                one_freq = self._start_freq * i + self._step_freq
            for j in range(121):
                rx_data += struct.pack("H", one_freq)
                rx_data += struct.pack("H", 0)
                # rx_data += struct.pack("H", one_freq)
                rx_data += struct.pack("H", 7)
                rx_data += struct.pack("H", j * 4)
                # rx_data += struct.pack("H", 7)
        for i in range(remain_count):
            rx_data += struct.pack("H", 0)
            rx_data += struct.pack("H", 0)
            rx_data += struct.pack("H", 0)
            rx_data += struct.pack("H", 0)
        print(rx_data)
        # print(len(rx_data))
        # print(rx_data)
        rx_data = self.change_bytes_with_4(data=rx_data)
        self.send_udp_freq_cail_data(data=rx_data)
        rx_tail = self.change_bytes_with_4(data=rx_tail)
        print(len(rx_tail))
        self.send_udp_freq_cail_data(data=rx_tail)
        self._thread = None
        print("发送完成")

    def set_sg_link(self, link_ena: bool, ip_str: Optional[str] = None):
        print(222, link_ena)
        self._target_addr = (ip_str, UDP_PORT)
        if link_ena and ip_str:
            self._udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._link_visa_instr(ip_str)
        else:
            self._close_instr()
            self._udp_client = None
        # self._sign.sg_online.emit(self._is_link)

    def send_visa_idn(self):
        if self.is_link():
            print(self._query_visa_cmd(f'*IDN?'))

    def send_visa_reset(self):
        if self.is_link():
            print(self._write_visa_cmd(f'*RST'))

    def send_visa_freq_cmd(self, freq: float):
        """unit:Hz"""
        if self.is_link():
            self.update_param_freq(freq)
            self._write_visa_cmd(f':FREQ {freq}HZ;')

    def send_visa_pow_cmd(self, power: float):
        """power_ex:-2dbm"""
        if self.is_link():
            self.update_param_pow(power)
            self._write_visa_cmd(f':POW {power}dbm;')

    def send_visa_ena_cmd(self, ena: bool):
        if self.is_link():
            self.update_param_ena(ena)
            ena_str = 'ON' if self._ena else 'OFF'
            self._write_visa_cmd(f':OUTP {ena_str};')

    def update_param_pow(self, power: float):
        self._pow = power

    def update_param_freq(self, freq: float):
        self._freq = freq

    def update_param_ena(self, ena: bool):
        self._ena = ena

    def get_power(self) -> float:
        return self._pow

    def get_freq(self) -> float:
        return self._freq

    # UDP_CMD
    def send_udp_freq_cmd(self, freq_mhz: int):
        data_bytes = struct.pack('<i', int(freq_mhz))
        cmd = UDP_HEAD + UDP_WRITE + UDP_FUNC_RF_FREQ + data_bytes + UDP_END
        self._send_udp_cmd(cmd)

    def send_udp_rf_att_cmd(self, rf_att: int):
        data_bytes = struct.pack('<i', int(rf_att))
        cmd = UDP_HEAD + UDP_WRITE + UDP_FUNC_RF_ATT + data_bytes + UDP_END
        self._send_udp_cmd(cmd)

    def send_udp_freq_cail_data(self, data: bytes):
        # for i in range(int(len(data) / 1024)):
        #     rx_bytes = UDP_HEAD + data[i * 1024: (i + 1): 1024]
        # print(f"data={data}")
        rx_bytes = UDP_HEAD + data
        # print(f"rx_bytes={rx_bytes}")
        self._send_udp_cmd(cmd=rx_bytes)

    def send_udp_freq_stop_cmd(self):
        """
        :param freq_mhz: unit: MHz not mHz
        :return:
        """
        data_bytes = struct.pack("<i", 0)
        cmd = CMD_UDP_HEAD + UDP_WRITE + UDP_FUNC_SET_FREQ_STOP + data_bytes + UDP_END
        self._send_udp_cmd(cmd=cmd)

    def send_udp_cal_start(self):
        print(1)
        data_bytes = struct.pack("<i", 0)
        cmd = CMD_UDP_HEAD + UDP_WRITE + UDP_FUNC_SET_CAL_START + data_bytes + UDP_END
        self._send_udp_cmd(cmd=cmd)

    def is_link(self) -> bool:
        return self._is_link

    def set_freq_start(self, freq: int):
        """
        :param freq: UNIT:MHz
        :return:
        """
        self._start_freq = freq

    def set_freq_stop(self, freq: int):
        self._stop_freq = freq

    def set_freq_step(self, freq: int):
        self._step_freq = freq

    def set_thread_start(self):
        self._thread = Thread(target=self._working, daemon=True)
        self._thread.start()

    def set_thread_stop(self):
        self._thread = None

    def _link_visa_instr(self, ip_str):
        try:
            visa_str = self.generate_visa_name(ip_str)
            self._visa_device = pyvisa.ResourceManager().open_resource(visa_str)
        except pyvisa.errors.VisaIOError:
            print('ERROR={信号源设备未找到或未连接}')
            self._is_link = False
        else:
            self._is_link = True

    def _write_visa_cmd(self, data: str):
        if self._visa_device and self.is_link():
            try:
                time.sleep(0.002)
                self._visa_device.write(data)
            except pyvisa.errors.VisaIOError:
                self._is_link = False
                # self._sign.sg_online.emit(False)

    def _query_visa_cmd(self, cmd: str) -> str:
        rx_data = '0'
        if self.is_link() and '?' in cmd:
            try:
                rx_data = self._visa_device.query(cmd)
            except pyvisa.errors.VisaIOError:
                self._is_link = False
                # self._sign.sg_online.emit(False)
        return rx_data

    def _close_instr(self):
        try:
            self._visa_device.close()
        except Exception as e:
            print('ERROR={设备早就断开了},', e)
            self._is_link = False
        self._is_link = False
        self._target_addr = None
        self._visa_device = None

    def _send_udp_cmd(self, cmd):
        if self._target_addr and self._is_link:
            self._udp_client.sendto(cmd, self._target_addr)
            # time.sleep(0.005)
            # print("UDP 有问题", e)
            # self._is_link = False
            # self._sign.sg_online.emit(False)

    @staticmethod
    def generate_visa_name(ip_str: str) -> str:
        return f'TCPIP0::{ip_str}::{VISA_PORT}::SOCKET'


if __name__ == '__main__':
    # 定义要连接的服务器IP和端口号
    SERVER_IP = '192.9.16.1'
    sg = Sg()
    sg.set_sg_link(True, SERVER_IP)

    sg.set_freq_start(freq=600)
    sg.set_freq_stop(freq=600)
    sg.set_freq_step(10)
    sg.set_thread_start()
    time.sleep(0.1)
    sg.send_udp_cal_start()

    # sg.send_udp_freq_stop_cmd()

    # sg.send_visa_freq_cmd(1e8)
    # sg.send_visa_pow_cmd(10)
    while 1:
        time.sleep(1)
    # sg.set_sg_link(False)
