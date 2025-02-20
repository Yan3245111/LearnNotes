import ctypes
import os

# 加载 ComuPCIe DLL
DLL_PATH = os.path.abspath("ComuPCIe.dll")
comupcie_dll = ctypes.CDLL(DLL_PATH)

# 定义常量
DMA_SIZE = 4 * 1024 * 1024  # 4MB DMA 缓冲区大小


# 枚举 CardType
class CardType:
    TypeUnDef = 0x0
    TypeDRFMV7 = 0xD23  # 三个FPGA
    TypeIntf = 0xD21  # 接口板
    TypeSATA = 0xD22  # 存储板


# ComuPCIe 类的 Python 封装
class ComuPCIe:
    def __init__(self, card_index: int):
        self.card_index = ctypes.c_uint(card_index)
        # 创建 C++ 类的实例
        self.instance = comupcie_dll.ComuPCIe(self.card_index)

    # 打开设备
    def open(self) -> int:
        result = self.instance.open()
        print(f"open() 结果: {result}")
        return result

    # 检查设备是否已打开
    def is_open(self) -> bool:
        result = self.instance.isOpen()
        print(f"isOpen() 结果: {bool(result)}")
        return bool(result)

    # 关闭设备
    def close(self) -> int:
        result = self.instance.close()
        print(f"close() 结果: {result}")
        return result

    # PCIe 设备复位
    def dev_reset(self) -> int:
        result = self.instance.devReset()
        print(f"devReset() 结果: {result}")
        return result

    # 写入寄存器
    def write_reg(self, addr_offset: int, value: int, bar_index: int = 0) -> int:
        result = self.instance.writeReg(
            ctypes.c_ulong(addr_offset),
            ctypes.c_int(value),
            ctypes.c_uint(bar_index)
        )
        print(f"writeReg() 结果: {result}")
        return result

    # 读取寄存器
    def read_reg(self, addr_offset: int, bar_index: int = 0) -> int:
        value = ctypes.c_int()
        result = self.instance.readReg(
            ctypes.c_ulong(addr_offset),
            ctypes.byref(value),
            ctypes.c_uint(bar_index)
        )
        if result == 0:
            print(f"readReg() 成功: 值 = {value.value}")
        else:
            print(f"readReg() 失败: 结果 = {result}")
        return value.value if result == 0 else None

    # 加载 bit 文件到 FPGA
    def load_bit_program(self, file_path: str, v7_index: int, per_size: int) -> int:
        if not os.path.isfile(file_path):
            print(f"文件不存在: {file_path}")
            return -1

        # 文件路径必须为字节字符串
        file_path_bytes = file_path.encode('utf-8')

        result = self.instance.loadBitProgram(
            file_path_bytes,
            ctypes.c_int(v7_index),
            ctypes.c_int(per_size)
        )
        print(f"loadBitProgram() 结果: {result}")
        return result

    # 写入数据到 PCIe 缓冲区
    def write_buffer(self, data: bytes, timeout: int = 2000000) -> int:
        data_len = len(data)
        buf = (ctypes.c_ubyte * data_len)(*data)
        result = self.instance.writeBuffer(buf, ctypes.c_uint(data_len), ctypes.c_uint(timeout))
        print(f"writeBuffer() 结果: {result}")
        return result

    # 从 PCIe 读取数据到缓冲区
    def read_buffer(self, size: int, timeout: int = 2000000) -> bytes:
        buf = (ctypes.c_ubyte * size)()
        result = self.instance.readBuffer(buf, ctypes.c_uint(size), ctypes.c_uint(timeout))
        if result == 0:
            print(f"readBuffer() 成功")
            return bytes(buf)
        else:
            print(f"readBuffer() 失败: 结果 = {result}")
            return None


if __name__ == '__main__':
    pass
