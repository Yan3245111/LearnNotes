# 2023.6.3

* ui_work.h 参数列表结构体里列表num类型为unit8 导致255以上的行数有问题
  如果改为unit16 编译不过去
* ui_work.h LIST_START_NUM 146
  * 以上2个问题是因为空间不够，把lv_conf里的空间改小即可
***
* ui_work.h 参数列表value/default_value 类型为int 以后存文件的时候可能需要char类型
  到时候应该需要单独建一个struct管理文件
* pulse输入数值卡死 
  * 原因1：param_no 的定义不对，一边char，一边int
  * 原因2：定义了宏定义，但是还是用的死数来做判断
  * 串口发送的时候 param_no定义的是u8，实际应该用16，发的时候多加了一位，然后把地址指针发过去的
    uint8_t *Num;
    uint8_t Array[5];
    Num = Array+1;
    uint16_t U16 = 300;
    uint16_t U17 = 0;
    memcpy(Num, &U16, 2);
    memcpy(&U17,Array+1,2);