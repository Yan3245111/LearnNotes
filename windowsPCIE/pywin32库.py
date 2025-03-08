import win32file
import win32con

# 安装的驱动打印出来的PCI设备必须是注册成\\.\开头的才可以正常调用，否则无法通信成功

# 打开设备
device_name = r'\\.\PCIE_DEVICE'
handle = win32file.CreateFile(
    device_name,
    win32con.GENERIC_READ | win32con.GENERIC_WRITE,
    0,
    None,
    win32con.OPEN_EXISTING,
    0,
    None
)

if handle == win32file.INVALID_HANDLE_VALUE:
    raise Exception("Failed to open device")

# 定义控制代码
IOCTL_READ_REGISTER = 0x8000
IOCTL_WRITE_REGISTER = 0x8001

# 读写寄存器
input_buffer = b'\x00\x10\x00\x00'  # 寄存器地址
output_buffer = win32file.AllocateReadBuffer(4)
win32file.DeviceIoControl(handle, IOCTL_READ_REGISTER, input_buffer, output_buffer, 0)
print(f"Register value: {int.from_bytes(output_buffer, 'little')}")

input_buffer = b'\x00\x10\x00\x00\x34\x12\x00\x00'  # 寄存器地址和值
win32file.DeviceIoControl(handle, IOCTL_WRITE_REGISTER, input_buffer, None, 0)

# 关闭设备
win32file.CloseHandle(handle)