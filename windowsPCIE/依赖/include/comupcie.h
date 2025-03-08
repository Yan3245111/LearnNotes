#ifndef COMUPCIE_H
#define COMUPCIE_H

#ifdef _WIN32
#include <windows.h>
#endif

#include <stdio.h>
#include <sys/stat.h>

#include <QDebug>

#if defined(COMUPCIE_LIBRARY)
#  define COMUPCIESHARED_EXPORT __declspec(dllexport)
#else
#  define COMUPCIESHARED_EXPORT __declspec(dllimport)
#endif


#define DMA_SIZE (4*1024*1024)

class COMUPCIESHARED_EXPORT ComuPCIe
{
public:
    enum CardType{
        TypeUnDef = 0x0,
        TypeDRFMV7 = 0xD23,             ///<三个FPGA
        TypeIntf = 0xD21,               ///<接口板
        TypeSATA = 0xD22,               ///<存储板
    };

    enum DRFMType{

    };

    ComuPCIe(uint cardIndex);
    virtual ~ComuPCIe();

    /**
     * @brief open First Step for each card, Open the card
     * @return 0:success; -1:card already open; -2:Can't create file; -3:mapEvent err; -4:mapMem err.
     */
    int open();

    /**
     * @brief isOpen
     * @return
     */
    bool isOpen();

    /**
     * @brief close Last Step for each card
     * @return 0:success; -1:Err
     */
    int close();

    /**
     * @brief devReset PCIe reset
     * @return
     */
    int devReset();

    /**
     * @brief writeReg
     * @param barIndex
     * @param addrOffset
     * @param value
     * @return 0:success; -1:Err
     */
    int writeReg(unsigned long addrOffset, int value, uint barIndex = 0);

    /**
     * @brief readReg
     * @param barIndex
     * @param addrOffset
     * @param value
     * @return 0:success; -1:Err
     */
    int readReg(unsigned long addrOffset, int &value, uint barIndex = 0);

    /**
     * @brief writeBuffer Write data from  PC to PCIe
     * @param pBuf
     * @param dataLen 0<dataLen<4M && 0==dataLen%128
     * @param timeOut
     * @return 0:success; -1:param err; -2:time out
     */
    int writeBuffer(void* pBuf, unsigned int dataLen, unsigned int timeOut = 2000000);

    /**
     * @brief readBuffer Read data from pcie to PC
     * @param pBuf
     * @param dataLen 0<dataLen<4M && 0==dataLen%128
     * @param timeOut
     * @return 0:success; -1:param err; -2:time out
     */
    int readBuffer(void* pBuf, unsigned int dataLen, unsigned int timeOut = 2000000);

    /**
     * @brief cardType
     * @return
     */
    CardType cardType();

    /**
     * @brief reset
     */
    void reset();

    /**
     * @brief loadBitProgram load Bit Program to FPGA
     * @param filePath bit file path
     * @param v7Index 0:V7_1 1:V7_2
     * @param perSize 256/512/1024/2048/4096
     * @return -1: get bitFile info err; -2: bit file open err; -3: DMA err; -4:time out
     */
    int loadBitProgram(const char *filePath, int v7Index, int perSize);

private:
    int mapEvent();
    int mapMem();
    int unMapMem();
private:
    uint m_cardIndex;               ///<Card Index
    CardType m_cardType;
    unsigned int   m_uiAddCnt;      ///<Count of memory to DMA
    unsigned int m_uiAddLen;        ///<Size of each memory to DMA
    unsigned char* m_pAdd[2];       ///<Addr of each memory to DMA
#ifdef _WIN32
    HANDLE m_hDv;
    HANDLE  m_Event;
#endif


};

#endif // COMUPCIE_H
