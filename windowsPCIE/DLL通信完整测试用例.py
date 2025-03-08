import ctypes

# 加载 DLL
pcie_dll = ctypes.CDLL("MyWrapper.dll")

# 定义函数参数和返回类型
pcie_dll.ComuPCIe_new.argtypes = [ctypes.c_uint]
pcie_dll.ComuPCIe_new.restype = ctypes.c_void_p

pcie_dll.ComuPCIe_delete.argtypes = [ctypes.c_void_p]
pcie_dll.ComuPCIe_delete.restype = None

pcie_dll.ComuPCIe_open.argtypes = [ctypes.c_void_p]
pcie_dll.ComuPCIe_open.restype = ctypes.c_int

pcie_dll.ComuPCIe_close.argtypes = [ctypes.c_void_p]
pcie_dll.ComuPCIe_close.restype = ctypes.c_int

pcie_dll.ComuPCIe_writeReg.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_int, ctypes.c_uint]
pcie_dll.ComuPCIe_writeReg.restype = ctypes.c_int

pcie_dll.ComuPCIe_readReg.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(ctypes.c_int), ctypes.c_uint]
pcie_dll.ComuPCIe_readReg.restype = ctypes.c_int

pcie_dll.ComuPCIe_cardType.argtypes = [ctypes.c_void_p]
pcie_dll.ComuPCIe_cardType.restype = ctypes.c_int

pcie_dll.ComuPCIe_reset.argtypes = [ctypes.c_void_p]
pcie_dll.ComuPCIe_reset.restype = None

pcie_dll.ComuPCIe_writeBuffer.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]
pcie_dll.ComuPCIe_writeBuffer.restype = ctypes.c_int

pcie_dll.ComuPCIe_readBuffer.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint]
pcie_dll.ComuPCIe_readBuffer.restype = ctypes.c_int

pcie_dll.ComuPCIe_loadBitProgram.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
pcie_dll.ComuPCIe_loadBitProgram.restype = ctypes.c_int

# 初始化
pci = pcie_dll.ComuPCIe_new(0)
if not pci:
    print("Failed to create PCIe object!")
    exit(1)

# 打开
if pcie_dll.ComuPCIe_open(pci) != 0:
    print("Failed to open PCIe device!")
    pcie_dll.ComuPCIe_delete(pci)
    exit(1)

print("PCIe device opened successfully.")
print(f"Device Type: {pcie_dll.ComuPCIe_cardType(pci)}")

# 复位
pcie_dll.ComuPCIe_reset(pci)
print("Device reset.")

# 测试寄存器
write_value = 42
read_value = ctypes.c_int()
pcie_dll.ComuPCIe_writeReg(pci, 0x100, write_value, 0)
pcie_dll.ComuPCIe_readReg(pci, 0x100, ctypes.byref(read_value), 0)
print(f"Register Read: {read_value.value}")

# 测试缓冲区
buffer_size = 1024
write_buf = (ctypes.c_ubyte * buffer_size)(*([0xAA] * buffer_size))
read_buf = (ctypes.c_ubyte * buffer_size)()

pcie_dll.ComuPCIe_writeBuffer(pci, write_buf, buffer_size, 2000)
pcie_dll.ComuPCIe_readBuffer(pci, read_buf, buffer_size, 2000)
print("Buffer Test Passed!" if list(write_buf) == list(read_buf) else "Buffer Mismatch!")

# 关闭
pcie_dll.ComuPCIe_close(pci)
pcie_dll.ComuPCIe_delete(pci)
print("PCIe device closed.")
