#ifndef MYWRAPPER_H
#define MYWRAPPER_H

#include "pcielib.h"

#ifdef _WIN32
#include <windows.h>
#endif

ComuPCIe* ComuPCIe_new(uint cardIndex) {
    return new ComuPCIe(cardIndex);
}

// 删除 PCIe 对象
void ComuPCIe_delete(ComuPCIe* pci) {
    delete pci;
}

// 打开 PCIe 设备
int ComuPCIe_open(ComuPCIe* pci) {
    if (pci == nullptr) return -1;
    return pci->open();
}

// 判断 PCIe 设备是否已打开
bool ComuPCIe_isOpen(ComuPCIe* pci) {
    if (pci == nullptr) return false;
    return pci->isOpen();
}

// 关闭 PCIe 设备
int ComuPCIe_close(ComuPCIe* pci) {
    if (pci == nullptr) return -1;
    return pci->close();
}

// 写寄存器
int ComuPCIe_writeReg(ComuPCIe* pci, unsigned long addrOffset, int value, uint barIndex) {
    if (pci == nullptr) return -1;
    return pci->writeReg(addrOffset, value, barIndex);
}

// 读寄存器
int ComuPCIe_readReg(ComuPCIe* pci, unsigned long addrOffset, int* value, uint barIndex) {
    if (pci == nullptr || value == nullptr) return -1;
    return pci->readReg(addrOffset, *value, barIndex);
}

// 写数据到 PCIe
int ComuPCIe_writeBuffer(ComuPCIe* pci, void* pBuf, unsigned int dataLen, unsigned int timeOut) {
    if (pci == nullptr || pBuf == nullptr) return -1;
    return pci->writeBuffer(pBuf, dataLen, timeOut);
}

// 从 PCIe 读取数据
int ComuPCIe_readBuffer(ComuPCIe* pci, void* pBuf, unsigned int dataLen, unsigned int timeOut) {
    if (pci == nullptr || pBuf == nullptr) return -1;
    return pci->readBuffer(pBuf, dataLen, timeOut);
}

// 加载 Bit 文件到 FPGA
int ComuPCIe_loadBitProgram(ComuPCIe* pci, const char* filePath, int v7Index, int perSize) {
    if (pci == nullptr || filePath == nullptr) return -1;
    return pci->loadBitProgram(filePath, v7Index, perSize);
}

// 重置设备
void ComuPCIe_reset(ComuPCIe* pci) {
    if (pci != nullptr) {
        pci->reset();
    }
}

#endif
