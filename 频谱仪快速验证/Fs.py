import pyvisa
import time
from typing import Optional

"""
ref 和 中心频率要一直更改

"""


class Fs:

    def __init__(self):
        self._visa_device = None
        self._is_keysight = True
        self._ts_delay = int()
        self._freq = float()  # unit:hz
        self._init_span, self._init_vbw, self._init_rbw, self._init_rel = float(), float(), float(), float()
        self._init_name, self._init_save_path = str(), str()
        self._init_delta_m = float()
        self._is_link = False
        self._ip = str()

    def set_visa_link(self, link_ena: bool, ip_str: Optional[str] = None):
        print(f'link [{link_ena}],ip {ip_str}')
        self._ip = ip_str
        if link_ena and ip_str:
            self._link_visa_instr(ip_str)
        else:
            self._close_instr()

    def get_cur_ip(self) -> str:
        return self._ip

    def send_freq_cmd(self, freq_hz: float):
        """unit:Hz"""
        self._freq = freq_hz
        self._write_visa_cmd(f':FREQ:CENT {self._freq}Hz;')

    def set_fft(self):
        self._write_visa_cmd(data=':FREQ:SPAN 100000Hz')
        self._write_visa_cmd(data=':BAND:VID 1000Hz')
        self._write_visa_cmd(data=':BAND 1000Hz')
        self._write_visa_cmd(data=':DISP:WIND:TRAC:Y:RLEV 20dbm')
        self._write_visa_cmd(data=':SWE:TYPE FFT')  # 设置fft模式
        # self._write_visa_cmd(data=":SWE:TYPE:AUTO OFF")  # fft 自动模式
        # self._write_visa_cmd(data=':DISP:WIND:MAM OFF')  # 关闭测量接口
        # self._write_visa_cmd(data=':DISP:GRAT OFF')  # 关闭网格显示
        self._write_visa_cmd(data='DISP:ENAB OFF')  # 关闭屏幕显示
        # self._write_visa_cmd(data=':SWE:TIME 1ms')  # 扫描时间
        self._write_visa_cmd(data=':CALC:MARK:CPS OFF')   # 关闭峰值搜索
        # self._write_visa_cmd(data=":SWE:POIN 5001")  # 设置为15001个点时候，扫描可以到1ms

    def send_span_cmd(self, span_hz: float):
        self._write_visa_cmd(f':FREQ:SPAN {span_hz}Hz;')

    def send_rbw_cmd(self, rbw_hz: float):
        self._write_visa_cmd(f':BAND {rbw_hz}Hz;')

    def send_vbw_cmd(self, vbw_hz: float):
        self._write_visa_cmd(f':BAND:VID {vbw_hz}Hz;')

    def send_rel_cmd(self, ref: float):
        self._init_rel = ref
        self._write_visa_cmd(f':DISP:WIND:TRAC:Y:RLEV {ref}dbm;')

    def get_ref(self) -> float:
        return self._init_rel

    def get_freq(self) -> float:
        return self._freq

    def set_fast_measure_mode(self):
        self._write_visa_cmd(data=f'CALC:FPOW:POW:RES')
        self._write_visa_cmd(data=f"CALC:FPOW:POW:DEF "
                                  f"DCCoupled=True,"
                                  f"ElecAttBypass=False,"
                                  f"MechAttenuation=10,"
                                  f"PreSelectorOffset=0,"
                                  f"UsePreSelector=False,"
                                  f"ExternalReferenceFrequency=10000000,"
                                  f"FrequencyReferenceSource=AutoExternalFrequencyReference,"
                                  f"IFType=WideBandIF,"
                                  f"LOMode=SLW,"
                                  f"CenterFrequency={40000000000},"
                                  f"DetectorType=RmsAverage,"
                                  f"Bandwidth=[100000000],"
                                  f"OffsetFrequency=[0],"
                                  f"Function=[BandPower],"
                                  f"FilterType=[IBW],"
                                  f"MeasurementMethod=HardwareFFT,"
                                  f"TriggerSource=Free")

        power = self._query_visa_cmd(cmd='CALC:FPOW:POW?;')
        print(power)

    def read_peak_point(self):
        # self.set_sweep_once()
        self._write_visa_cmd(':CALC:MARK1:MAX:PEAK;')
        # self._write_visa_cmd("CALC:MARK1:MAX;")
        p_x = float(self._query_visa_cmd(':CALC:MARK1:X?;'))
        p_y = float(self._query_visa_cmd(':CALC:MARK1:Y?;'))
        return [p_x, p_y]

    def read_peak_point_wait(self):
        self._write_visa_cmd(':CALC:MARK1:MAX:PEAK;*WAI;')
        # self._write_visa_cmd("CALC:MARK1:MAX;")
        p_x = float(self._query_visa_cmd(':CALC:MARK1:X?;*WAI;'))
        p_y = float(self._query_visa_cmd(':CALC:MARK1:Y?;*WAI;'))
        return [p_x, p_y]

    def set_sweep_once(self, ena: bool):
        data = ":INIT:CONT ON;" if ena else ":INIT:CONT OFF;"
        self._write_visa_cmd(data=data)
        self._write_visa_cmd(data=':TRAC2:UPD 0')

    def fetch_fast_pow(self):
        power = float(self._query_visa_cmd(":CALC:FPOW:POW1:FETC?"))
        print(power)

    def set_fft_high(self):
        self._write_visa_cmd(data=':IF:GAIN:SWEP ON')
        self._write_visa_cmd(data=":IF:GAIN:FFT HIGH")

    def is_link(self) -> bool:
        return self._is_link

    def get_fs_info(self) -> list:
        return [self._freq]

    def is_keysight_instr(self):
        info_str = self._query_visa_cmd("*IDN?")
        if "Keysight".upper() in info_str.upper():
            self._is_keysight = True
        else:
            self._is_keysight = False

    def _link_visa_instr(self, ip_str):
        try:
            visa_str = self.generate_visa_name(ip_str)
            print(visa_str)
            self._visa_device = pyvisa.ResourceManager().open_resource(visa_str)
        except pyvisa.errors.VisaIOError:
            print('ERROR={频谱仪设备未找到或未连接}')
            self._is_link = False
        else:
            self._is_link = True
            self.is_keysight_instr()

    def _write_visa_cmd(self, data: str):
        if self._visa_device and self.is_link():
            try:
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
            print('ERROR={频谱仪设备早就断开了},', e)
            self._is_link = False
        self._is_link = False
        self._visa_device = None

    @staticmethod
    def generate_visa_name(ip_str: str) -> str:
        return f'TCPIP0::{ip_str}::inst0::INSTR'

    def fft_mode(self):
        self._write_visa_cmd(data=':SWE:TYPE FFT')


if __name__ == '__main__':
    import time
    "K-N9020B-30098.local"
    print(pyvisa.ResourceManager().list_resources())
    ip = "192.168.1.20"
    fs = Fs()
    fs.set_visa_link(link_ena=True, ip_str=ip)
    fs.send_freq_cmd(freq_hz=38.52 * 1e9)
    fs.set_fft()
    # fs.set_fft_high()
    # fs.send_span_cmd(20000)
    # fs.send_rbw_cmd(rbw_hz=3000)
    # fs.send_vbw_cmd(vbw_hz=3000)
    while 1:
        time.sleep(1)
        ts = time.time()
        x, y = fs.read_peak_point()
        print(f"time={time.time() - ts}, freq={x}, ampl={y}")
        # fs.set_fast_measure_mode()
        # print(f'time={time.time() - ts}')
