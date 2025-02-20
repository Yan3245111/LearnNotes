import os
import win32file

device_name = r"\\.\YourDeviceName"

# 打开设备句柄
handle = win32file.CreateFile(
    device_name,
    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
    0,
    None,
    win32file.OPEN_EXISTING,
    0,
    None
)

# 读写操作
try:
    # 读操作
    buffer = win32file.DeviceIoControl(handle, 0x80002000, None, 256)
    print("Read data:", buffer)

    # 写操作 (示例数据)
    data = b"\xDE\xAD\xBE\xEF"
    win32file.DeviceIoControl(handle, 0x80002001, data, 0)
    print("Write successful")
finally:
    win32file.CloseHandle(handle)


import os
# 列出pci设备
print([f for f in os.listdir(r'\\.\') if f.startswith(PCI)')])

try:
    buffer = win32file.DeviceIoControl(handle, 0x80002000, None, 256)
except Exception as e:
    print(f"Read failed: {e}")


# 第二种方法 找刘康要dll文件，测试用例智铭的mynotes里有
