#ifndef PCIELIB_H
#define PCIELIB_H

#ifdef _WIN32
#include <windows.h>
#endif

#include "pcielib_global.h"
#include "PCIEDLL/include/comupcie.h"
#include "PCIEDLL/include/DeviceMapMacro.h"

// 使用 extern "C" 以便 Python 调用时避免 C++ 名字修饰
extern "C" {

    // 创建 PCIe 对象
    __declspec(dllexport) ComuPCIe* ComuPCIe_new(uint cardIndex);

    // 删除 PCIe 对象
    __declspec(dllexport) void ComuPCIe_delete(ComuPCIe* pci);

    // 打开 PCIe 设备
    __declspec(dllexport) int ComuPCIe_open(ComuPCIe* pci);

    // 判断 PCIe 设备是否已打开
    __declspec(dllexport) bool ComuPCIe_isOpen(ComuPCIe* pci);

    // 关闭 PCIe 设备
    __declspec(dllexport) int ComuPCIe_close(ComuPCIe* pci);

    // 写寄存器
    __declspec(dllexport) int ComuPCIe_writeReg(ComuPCIe* pci, unsigned long addrOffset, int value, uint barIndex);

    // 读寄存器
    __declspec(dllexport) int ComuPCIe_readReg(ComuPCIe* pci, unsigned long addrOffset, int* value, uint barIndex);

    // 写数据到 PCIe
    __declspec(dllexport) int ComuPCIe_writeBuffer(ComuPCIe* pci, void* pBuf, unsigned int dataLen, unsigned int timeOut);

    // 从 PCIe 读取数据
    __declspec(dllexport) int ComuPCIe_readBuffer(ComuPCIe* pci, void* pBuf, unsigned int dataLen, unsigned int timeOut);

    // 加载 Bit 文件到 FPGA
    __declspec(dllexport) int ComuPCIe_loadBitProgram(ComuPCIe* pci, const char* filePath, int v7Index, int perSize);

    // 重置设备
    __declspec(dllexport) void ComuPCIe_reset(ComuPCIe* pci);
}
#endif // MYWRAPPER_H
