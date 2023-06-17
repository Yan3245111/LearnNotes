* stm32f407z USB正点原子移植
* 将此4个文件粘贴到工程即可
* 在main.c 文件添加以下代码即可
```
USBH_HOST  USB_Host;
USB_OTG_CORE_HANDLE  USB_OTG_Core;
FRESULT res;  
FRESULT res1;
FRESULT res2; 
FATFS fs;
FIL fp;//文件对象DRESULT res;
char *write_text="FATFS test success!";
unsigned int write_bytes=0;
char read_buff[512];
unsigned int read_bytes=0;

u8 USH_User_App(void)
	{ 
		u8 readbuff[10];
		res = f_mount(&fs, "2:", 1);
		u32 total,free;
		UINT buffNum;
		//res2=exf_getfree("2:",&total,&free);
		res2 = f_open(&fp,"2:123.txt",FA_OPEN_EXISTING | FA_READ);
			res = f_read(&fp, readbuff, sizeof(readbuff), &buffNum);
		//res1 = f_write(&fp,(char*)write_text,strlen(write_text),&write_bytes);
		f_close(&fp);
		f_mount(NULL, "2:", 1);
		return 1;
	}

void main()
{
    USBH_Init(&USB_OTG_Core,USB_OTG_FS_CORE_ID,&USB_Host,&USBH_MSC_cb,&USR_Callbacks);  
	while(1)
	{
        USBH_Process(&USB_OTG_Core, &USB_Host);
        delay_ms(1);
	}
}
```
