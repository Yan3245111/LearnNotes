import time
import struct
import socket
import pyvisa
from typing import Optional

UDP_PORT = 20481
VISA_PORT = 5025

# HEAD
UDP_HEAD = b'\x7e\x7e'
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

    def set_sg_link(self, link_ena: bool, ip_str: Optional[str] = None):
        print(222, link_ena)
        self._target_addr = (ip_str, UDP_PORT)
        if link_ena and ip_str:
            self._udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._link_visa_instr(ip_str)
        else:
            self._close_instr()
            self._udp_client = None

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
        self._freq = freq_mhz
        data_bytes = struct.pack('<i', int(freq_mhz))
        cmd = UDP_HEAD + UDP_WRITE + UDP_FUNC_RF_FREQ + data_bytes + UDP_END
        self._send_udp_cmd(cmd)

    def send_udp_rf_att_cmd(self, rf_att: int):
        data_bytes = struct.pack('<i', int(rf_att))
        cmd = UDP_HEAD + UDP_WRITE + UDP_FUNC_RF_ATT + data_bytes + UDP_END
        self._send_udp_cmd(cmd)

    def send_udp_if_att_cmd(self, if_att):
        data_bytes = struct.pack('<i', int(if_att))
        cmd = UDP_HEAD + UDP_WRITE + UDP_FUNC_IF_ATT + data_bytes + UDP_END
        self._send_udp_cmd(cmd)

    def send_udp_if_digital_att_cmd(self, if_digital_att):
        data_bytes = struct.pack('<i', int(if_digital_att))
        cmd = UDP_HEAD + UDP_WRITE + UDP_FUNC_IF_DIGITAL_ATT + data_bytes + UDP_END
        self._send_udp_cmd(cmd)

    def send_udp_ena_cmd(self, ena):
        data_bytes = struct.pack('<i', int(ena))
        cmd = UDP_HEAD + UDP_WRITE + UDP_FUNC_RF_ENA + data_bytes + UDP_END
        self._send_udp_cmd(cmd)

    def send_udp_pl_addr(self, addr):
        data_bytes = struct.pack('<i', int(addr))
        cmd = UDP_HEAD + UDP_WRITE + UDP_FUNC_PL_ADDR + data_bytes + UDP_END
        self._send_udp_cmd(cmd)

    def send_udp_pl_data(self, data):
        data_bytes = struct.pack('<i', int(data))
        cmd = UDP_HEAD + UDP_WRITE + UDP_FUNC_PL_DATA + data_bytes + UDP_END
        self._send_udp_cmd(cmd)

    def is_link(self) -> bool:
        return self._is_link

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

    def _query_visa_cmd(self, cmd: str) -> str:
        rx_data = '0'
        if self.is_link() and '?' in cmd:
            try:
                rx_data = self._visa_device.query(cmd)
            except pyvisa.errors.VisaIOError:
                self._is_link = False
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
    SERVER_IP = '192.9.18.136'
    sg = Sg()
    sg.set_sg_link(True, SERVER_IP)
    sg.send_visa_freq_cmd(1e9)
    sg.set_sg_link(False)
    # udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # udp_s.sendto(b'\x7e\x7e', (SERVER_IP, UDP_PORT))
    #
