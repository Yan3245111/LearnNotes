import time
import pyvisa
from threading import Thread, Timer

"""
自由模式：同一个频率 功率计可以不设频谱 只读是没问题的
1-设置频率 fect 读取 50ms左右，快速测量大概在3-4ms(同频点/功率)  *RST, SENS:MRAT FAST, FREQ {freq}hz, FETC?
    * 不同频率功率读取大概在30-40ms左右，但是信号源发送数据以后还要等待80ms才可以进行数据读取，总用时128ms一个点(48ms左右数据没问题)
2-设置频率 conf1 read1 55ms, 快速测量大概在6-7ms
TRIG模式：

"""


class PowerSensor:

    def __init__(self):
        self._device = None
        self._manager = pyvisa.ResourceManager()
        # PARAM
        self._freq = float()
        self._dev_name = str()
        self._list_name = list()
        self._is_online = False
        self._list_name = self._manager.list_resources()
        # THREAD
        self._thread = Thread(target=self._working, daemon=True)
        self._thread_switch = True
        self._thread.start()
        # TIMER
        self._timer = Timer(15, self._timer_count)

    # THREAD
    def _working(self):
        while self._thread_switch:
            if not self._list_name:
                self._list_name = self._manager.list_resources()
                # if self._list_name:
                #     self._sign.ps_name_list.emit(self._list_name)
            time.sleep(1)

    def _timer_count(self):
        # self._sign.ps_online.emit(1)
        self._is_online = True
        # self._send_cmd(cmd="SYST:PRES")
        # self._send_cmd(cmd="SENS:MRAT FAST")
        self._send_cmd(cmd="*WAI")
        # ----------**------------
        print("功率计连接成功")

    def connect_ps(self):
        if self._is_online and self._dev_name:
            self._is_online = False
            print("开始连接功率计")
            try:
                self._device = self._manager.open_resource(self._dev_name)
            except pyvisa.errors.VisaIOError:
                print('功率计连接失败')
                self._is_online = False
                if self._timer.is_alive():
                    self._timer.cancel()
                # self._sign.ps_online.emit(0)
            else:
                cmd = f'*RST'
                self._send_cmd(cmd=cmd)  # 加一个线程，30s后发送连接成功的信号
                print("功率计连接中，请等待")
                # self._sign.ps_online.emit(2)  # 2=正在连接中
                if self._timer.is_alive():
                    self._timer.cancel()
                self._timer = Timer(15, self._timer_count)
                self._timer.start()
        else:
            print("功率计断开连接")
            self._is_online = False
            self._device = None
            if self._timer.is_alive():
                self._timer.cancel()
            # self._sign.ps_online.emit(0)

    def _send_cmd(self, cmd: str):
        if self._device and self._is_online:
            self._device.write(cmd)

    def _read_cmd(self, cmd: str):
        if self._device and self._is_online:
            self._device.read(cmd)

    def _check_cmd(self, cmd: str) -> bytes:
        rx_data = bytes()
        if self._device and self._is_online and '?' in cmd:
            try:
                rx_data = self._device.query(cmd)
            except pyvisa.errors.VisaIOError as err:
                print('功率计读取错误，请重新读取')
        return rx_data

    def set_freq(self, freq: float):
        cmd = f'SENS:FREQ {freq} Hz'
        self._send_cmd(cmd=cmd)

    # 50ms
    def set_free_run_mode(self):
        self._send_cmd(cmd='SYST:PRES')
        self._send_cmd(cmd='SENS:FREQ 1 GHz')
        self._send_cmd(cmd='INIT:CONT ON')
        self._send_cmd(cmd='UNIT:POW W')
        self._send_cmd(cmd='FORM REAL')
        self._send_cmd(cmd='CAL:ZERO:AUTO OFF')
        self._send_cmd(cmd='CAL:AUTO OFF')
        self._send_cmd(cmd='SENS:AVER:SDET OFF')
        self._send_cmd(cmd='SENS:DET:FUNC NORM')
        self._send_cmd(cmd='SENS:MRAT FAST')
        self._send_cmd(cmd='TRIG:COUN 100')
        # power = self._check_cmd(cmd='FETC?')

    def set_trigger_mode(self):
        self._send_cmd(cmd='SYST:PRES')
        self._send_cmd(cmd="TRIG:SOUR EXT")
        self._send_cmd(cmd="OUTP:TRIG ON")
        self._send_cmd(cmd="SENS:MRAT FAST")

    # 50ms 左右
    def get_power(self) -> float:
        if self._is_online:
            # self._send_cmd(cmd="SENS:MRAT FAST")
            cmd = f'FETC?'
            # self._send_cmd(cmd="CONF1")
            # cmd = f'READ?'
            ampl = self._check_cmd(cmd=cmd)
            return float(ampl)

    def set_online(self):
        self._is_online = not self._is_online

    def set_dev_name(self, name: str):
        self._dev_name = name

    # GET
    def get_freq(self) -> float:
        return self._freq

    def get_device_list(self) -> tuple:
        return self._list_name

    def get_online(self) -> bool:
        return self._is_online and self._dev_name

    def exit(self):
        self._thread_switch = False
        self._manager.close()


if __name__ == '__main__':
    ps = PowerSensor()
    ps.set_online()
    ps.set_dev_name(ps._list_name[0])
    ps.connect_ps()
    # ps.set_trigger_mode()
    # freq = 1000000000
    while 1:
        if ps.get_online():
            ps.set_trigger_mode()
            break
            # while 1:
            #     # freq += 100000000
            #     # ps.set_freq(freq=freq)
            #     ts = time.time()
            #     power = ps.get_power()
            #     print(time.time() - ts)
            #     print(power)
            #     time.sleep(0.004)
        else:
            time.sleep(1)

