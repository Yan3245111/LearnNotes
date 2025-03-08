
import os
import ctypes

card_index = 0
reg_addr = 0x100
write_value = 42
read_value = ctypes.c_int()
bar_index = 0

path = os.path.abspath("PCIeLib.dll")

my_dll = ctypes.CDLL(path)

# 定义 ComuPCIe 对象的函数
my_dll.ComuPCIe_new.argtypes = [ctypes.c_uint]
my_dll.ComuPCIe_new.restype = ctypes.POINTER(ctypes.c_void_p)

my_dll.ComuPCIe_delete.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
my_dll.ComuPCIe_delete.restype = None

my_dll.ComuPCIe_writeReg.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_int, ctypes.c_uint]
my_dll.ComuPCIe_writeReg.restype = ctypes.c_int

my_dll.ComuPCIe_readReg.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(ctypes.c_int), ctypes.c_uint]
my_dll.ComuPCIe_readReg.restype = ctypes.c_int

# 创建 ComuPCIe 对象
pci_instance = my_dll.ComuPCIe_new(0)  # 传入卡号参数

# 调用 PCIe 函数
my_dll.ComuPCIe_open.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
my_dll.ComuPCIe_open.restype = ctypes.c_int

result = my_dll.ComuPCIe_open(pci_instance)
print(f"Open result: {result}")

# 写参数
my_dll.ComuPCIe_writeReg(pci_instance, reg_addr, write_value, bar_index)


# 读参数
if my_dll.ComuPCIe_readReg(pci_instance, reg_addr, ctypes.byref(read_value), bar_index) != 0:
    print("Failed to read register!")
else:
    print(f"Register read successfully. Value: {read_value.value}")

# 关闭 ComuPCIe 对象
my_dll.ComuPCIe_close.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
my_dll.ComuPCIe_close.restype = ctypes.c_int

close_result = my_dll.ComuPCIe_close(pci_instance)
print(f"Close result: {close_result}")

# 删除 ComuPCIe 对象
my_dll.ComuPCIe_delete(pci_instance)
