import ctypes
from ctypes import wintypes
import sys

# 定义 ULONG_PTR 类型
if sys.maxsize > 2**32:
    ULONG_PTR = ctypes.c_ulonglong  # 64 位系统
else:
    ULONG_PTR = ctypes.c_ulong      # 32 位系统

# 定义 GUID 结构体
class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8),
    ]

# 加载必要的 DLL
setupapi = ctypes.WinDLL('setupapi', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# 定义常量
DIGCF_DEFAULT = 0x00000001
DIGCF_PRESENT = 0x00000002
DIGCF_ALLCLASSES = 0x00000004
SPDRP_DEVICEDESC = 0x00000000
SPDRP_HARDWAREID = 0x00000001
INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

# 定义结构体
class SP_DEVINFO_DATA(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('ClassGuid', GUID),
        ('DevInst', wintypes.DWORD),
        ('Reserved', ULONG_PTR),
    ]

# 定义函数原型
SetupDiGetClassDevs = setupapi.SetupDiGetClassDevsW
SetupDiGetClassDevs.argtypes = [
    ctypes.POINTER(GUID),           # ClassGuid
    wintypes.LPCWSTR,               # Enumerator
    wintypes.HWND,                  # hwndParent
    wintypes.DWORD,                 # Flags
]
SetupDiGetClassDevs.restype = wintypes.HANDLE

SetupDiEnumDeviceInfo = setupapi.SetupDiEnumDeviceInfo
SetupDiEnumDeviceInfo.argtypes = [
    wintypes.HANDLE,                # DeviceInfoSet
    wintypes.DWORD,                 # MemberIndex
    ctypes.POINTER(SP_DEVINFO_DATA),# DeviceInfoData
]
SetupDiEnumDeviceInfo.restype = wintypes.BOOL

SetupDiGetDeviceRegistryProperty = setupapi.SetupDiGetDeviceRegistryPropertyW
SetupDiGetDeviceRegistryProperty.argtypes = [
    wintypes.HANDLE,                # DeviceInfoSet
    ctypes.POINTER(SP_DEVINFO_DATA),# DeviceInfoData
    wintypes.DWORD,                 # Property
    ctypes.POINTER(wintypes.DWORD), # PropertyRegDataType
    ctypes.c_void_p,                # PropertyBuffer
    wintypes.DWORD,                 # PropertyBufferSize
    ctypes.POINTER(wintypes.DWORD), # RequiredSize
]
SetupDiGetDeviceRegistryProperty.restype = wintypes.BOOL

SetupDiDestroyDeviceInfoList = setupapi.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.argtypes = [
    wintypes.HANDLE,                # DeviceInfoSet
]
SetupDiDestroyDeviceInfoList.restype = wintypes.BOOL

def get_device_names():
    # 获取设备信息集的句柄
    device_info_set = SetupDiGetClassDevs(
        None,                        # 所有设备类
        None,                        # 无特定设备
        None,                        # 无父窗口
        DIGCF_ALLCLASSES | DIGCF_PRESENT,
    )

    if device_info_set == INVALID_HANDLE_VALUE:
        print("Failed to get device information set.")
        return

    # 初始化设备信息结构
    device_info_data = SP_DEVINFO_DATA()
    device_info_data.cbSize = ctypes.sizeof(device_info_data)
    index = 0

    while True:
        # 枚举设备
        if not SetupDiEnumDeviceInfo(device_info_set, index, ctypes.byref(device_info_data)):
            break  # 没有更多设备时退出循环

        # 获取设备名称（设备描述）
        required_size = wintypes.DWORD()
        SetupDiGetDeviceRegistryProperty(
            device_info_set,
            ctypes.byref(device_info_data),
            SPDRP_DEVICEDESC,
            None,
            None,
            0,
            ctypes.byref(required_size),
        )

        buffer = (ctypes.c_wchar * required_size.value)()
        if SetupDiGetDeviceRegistryProperty(
            device_info_set,
            ctypes.byref(device_info_data),
            SPDRP_DEVICEDESC,
            None,
            buffer,
            required_size,
            None,
        ):
            device_desc = buffer.value
        else:
            device_desc = "Unknown"

        # 获取设备实例 ID
        SetupDiGetDeviceRegistryProperty(
            device_info_set,
            ctypes.byref(device_info_data),
            SPDRP_HARDWAREID,
            None,
            None,
            0,
            ctypes.byref(required_size),
        )

        buffer = (ctypes.c_wchar * required_size.value)()
        if SetupDiGetDeviceRegistryProperty(
            device_info_set,
            ctypes.byref(device_info_data),
            SPDRP_HARDWAREID,
            None,
            buffer,
            required_size,
            None,
        ):
            hardware_ids = buffer.value.split('\0')
        else:
            hardware_ids = []

        # 打印设备信息
        print(f"Device Name: {device_desc}")
        print(f"Hardware IDs: {hardware_ids}")
        print("-" * 40)

        index += 1

    # 释放设备信息集
    SetupDiDestroyDeviceInfoList(device_info_set)

if __name__ == "__main__":
    get_device_names()