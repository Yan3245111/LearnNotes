# 安装vs
# 在搜索输入vs找到vs2017或者相对应版本的交叉编译器 打开，输入以下命令，同样适用于lib文件
# dumpbin /exports your_library.dll
# dumpbin /dependents your_library.dll  查看依赖
# dumpbin /imports  your_library.dll  查看引用
# dumpbin /symbols your_library.dll (.lib)     查看符号

# WdfCoInstaller01009.dll 接口函数
#           1    0 00009C78 WdfCoInstaller
#           2    1 0000A110 WdfPostDeviceInstall
#           3    2 0000A1D8 WdfPostDeviceRemove
#           4    3 0000A0B4 WdfPreDeviceInstall
#           5    4 00009F08 WdfPreDeviceInstallEx
#           6    5 0000A17C WdfPreDeviceRemove


"""
          1    0 00001030 ??0ComuPCIe@@QEAA@AEBV0@@Z
          2    1 00001070 ??0ComuPCIe@@QEAA@I@Z
          3    2 000010B0 ??1ComuPCIe@@UEAA@XZ
          4    3 000010C0 ??4ComuPCIe@@QEAAAEAV0@AEBV0@@Z
          5    4 00003360 ??_7ComuPCIe@@6B@
          6    5 00001520 ?cardType@ComuPCIe@@QEAA?AW4CardType@1@XZ
          7    6 00001530 ?close@ComuPCIe@@QEAAHXZ
          8    7 00001610 ?devReset@ComuPCIe@@QEAAHXZ
          9    8 00001780 ?isOpen@ComuPCIe@@QEAA_NXZ
         10    9 00001790 ?loadBitProgram@ComuPCIe@@QEAAHPEBDHH@Z
         11    A 00001A60 ?mapEvent@ComuPCIe@@AEAAHXZ
         12    B 00001B00 ?mapMem@ComuPCIe@@AEAAHXZ
         13    C 00001D40 ?open@ComuPCIe@@QEAAHXZ
         14    D 00001F20 ?readBuffer@ComuPCIe@@QEAAHPEAXII@Z
         15    E 000020A0 ?readReg@ComuPCIe@@QEAAHKAEAHI@Z
         16    F 00002100 ?reset@ComuPCIe@@QEAAXXZ
         17   10 00002140 ?unMapMem@ComuPCIe@@AEAAHXZ
         18   11 00002190 ?writeBuffer@ComuPCIe@@QEAAHPEAXII@Z
         19   12 000022D0 ?writeReg@ComuPCIe@@QEAAHKHI@Z

"""
import ctypes
import os

# 加载 DLL 文件
dll_path = os.path.abspath("WdfCoInstaller01009.dll")
driver = ctypes.CDLL(dll_path)
driver.WdfCoInstaller()


# 定义函数原型 (根据 DLL 的实际函数签名)
# driver.DeviceRead.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
# driver.DeviceRead.restype = ctypes.c_int

# 准备调用参数
# device_id = 1
# buffer_size = 1024
# buffer = ctypes.create_string_buffer(buffer_size)

# 调用 DLL 函数
# result = driver.DeviceRead(device_id, buffer, buffer_size)

# 处理返回结果
# if result >= 0:
#     print("Read success:", buffer.value.decode('utf-8'))
# else:
#     print("Read failed with error code:", result)
