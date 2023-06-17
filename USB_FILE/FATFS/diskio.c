/*-----------------------------------------------------------------------*/
/* Low level disk I/O module skeleton for FatFs     (C)ChaN, 2013        */
/*-----------------------------------------------------------------------*/
/* If a working storage control module is available, it should be        */
/* attached to the FatFs via a glue function rather than modifying it.   */
/* This is an example of glue functions to attach various exsisting      */
/* storage control module to the FatFs module with a defined API.        */
/*-----------------------------------------------------------------------*/

#include "diskio.h"		/* FatFs lower layer API */
#include "usbh_usr.h"
//////////////////////////////////////////////////////////////////////////////////	 
//ѾԌѲֻ٩ѧϰʹԃìδޭط֟ѭࠉìһփԃԚǤ̼Ɏێԃ;
//ALIENTEK STM32F407ߪעѥ
//FATFS֗ӣ(diskio) Ƚ֯պë	   
//ֽ֣ԭؓ@ALIENTEK
//ܼ˵Û̳:www.openedv.com
//Դݨɕǚ:2014/5/15
//ѦѾúV1.1
//ѦȨ̹ԐìցѦҘ޿c
//Copyright(C) ڣםːчӭ֧ؓࠆܼԐО٫˾ 2014-2024
//All rights reserved									  
//********************************************************************************
//V1.1 20140722
//тնהUƌք֧Ԗ
////////////////////////////////////////////////////////////////////////////////// 	 


#define SD_CARD	 0  //SDߨ,߭ҪΪ0
#define EX_FLASH 1	//΢ҿflash,߭ҪΪ1
#define USB_DISK 2	//Uƌ,߭ҪΪ2

#define FLASH_SECTOR_SIZE 	512			  
//הԚW25Q128
//ǰ12Mؖޚٸfatfsԃ,12Mؖޚ۳,ԃԚզ؅ؖࠢ,ؖࠢռԃ3.09M.	ʣԠҿؖ,ٸࠍۧؔܺԃ	 			    
u16	    FLASH_SECTOR_COUNT=2048*12;	//W25Q1218,ǰ12MؖޚٸFATFSռԃ
#define FLASH_BLOCK_SIZE   	8     	//ÿٶBLOCKԐ8ٶʈȸ

//ԵʼۯՅƌ
DSTATUS disk_initialize (
	BYTE pdrv				/* Physical drive nmuber (0..) */
)
{
	u8 res=0;	    
	switch(pdrv)
	{
		case SD_CARD://SDߨ
		case USB_DISK://΢ҿflash
	  		if(USBH_UDISK_Status())return 0;	//Uƌlޓԉ٦,ղ׵ܘ1.رղ׵ܘ0		  
			else return 1;	 
		default:
			res=1; 
	}		 
	if(res)return  STA_NOINIT;
	else return 0; //Եʼۯԉ٦
}  

//ܱփՅƌ״̬
DSTATUS disk_status (
	BYTE pdrv		/* Physical drive nmuber (0..) */
)
{ 
	return 0;
} 

//ׁʈȸ
//drv:ՅƌҠۅ0~9
//*buff:˽ߝޓ˕ۺԥ˗ַ֘
//sector:ʈȸַ֘
//count:ѨҪׁȡքʈȸ˽
DRESULT disk_read (
	BYTE pdrv,		/* Physical drive nmuber (0..) */
	BYTE *buff,		/* Data buffer to store read data */
	DWORD sector,	/* Sector address (LBA) */
	UINT count		/* Number of sectors to read (1..128) */
)
{
	u8 res=0; 
    if (!count)return RES_PARERR;//countһŜֈԚ0ìرղ׵ܘӎ˽խϳ		 	 
	switch(pdrv)
	{
		case USB_DISK://Uƌ 
			res=USBH_UDISK_Read(buff,sector,count);	  
			break;
		default:
			res=1; 
	}
   //Ԧm׵ܘֵìݫSPI_SD_driver.cք׵ܘֵתԉff.cք׵ܘֵ
    if(res==0x00)return RES_OK;	 
    else return RES_ERROR;	   
}

//дʈȸ
//drv:ՅƌҠۅ0~9
//*buff:ע̍˽ߝ˗ַ֘
//sector:ʈȸַ֘
//count:ѨҪдɫքʈȸ˽
#if _USE_WRITE
DRESULT disk_write (
	BYTE pdrv,			/* Physical drive nmuber (0..) */
	const BYTE *buff,	/* Data to be written */
	DWORD sector,		/* Sector address (LBA) */
	UINT count			/* Number of sectors to write (1..128) */
)
{
	u8 res=0;  
    if (!count)return RES_PARERR;//countһŜֈԚ0ìرղ׵ܘӎ˽խϳ		 	 
	switch(pdrv)
	{
		case USB_DISK://Uƌ
			res=USBH_UDISK_Write((u8*)buff,sector,count); 
			break;
		default:
			res=1; 
	}
    //Ԧm׵ܘֵìݫSPI_SD_driver.cք׵ܘֵתԉff.cք׵ܘֵ
    if(res == 0x00)return RES_OK;	 
    else return RES_ERROR;	
}
#endif


//Ǥ̻ҭӎ˽քܱփ
 //drv:ՅƌҠۅ0~9
 //ctrl:࠘׆պë
 //*buff:ע̍/ޓ˕ۺԥȸָ֫
#if _USE_IOCTL
DRESULT disk_ioctl (
	BYTE pdrv,		/* Physical drive nmuber (0..) */
	BYTE cmd,		/* Control code */
	void *buff		/* Buffer to send/receive control data */
)
{
	DRESULT res;						  			     
	if(pdrv==SD_CARD)//SDߨ
	{
	    switch(cmd)
	    {
		    case CTRL_SYNC:
				res = RES_OK; 
		        break;	 
		    case GET_SECTOR_SIZE:
				*(DWORD*)buff = 512; 
		        res = RES_OK;
		        break;	 
		    default:
		        res = RES_PARERR;
		        break;
	    }
	}return res;
}


#endif

//ܱփʱݤ
//User defined function to give a current time to fatfs module      */
//31-25: Year(0-127 org.1980), 24-21: Month(1-12), 20-16: Day(1-31) */                                                                                                                                                                                                                                          
//15-11: Hour(0-23), 10-5: Minute(0-59), 4-0: Second(0-29 *2) */                                                                                                                                                                                                                                                

DWORD get_fattime (void)
{				 
	return 0;
}			 
