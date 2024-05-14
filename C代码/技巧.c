// exit使用：系统级别调用
exit(0)：正常退出
exit(1)：异常退出

// char / unsigned char 区别：主要是用char表示bytes的时候
// 表示bytes的时候 char会认为最高位是符号位，会帮忙扩展，下面举例说明
char buf[0] = 0xe7;
printf("%x\n", buf[0]);        // ffffffe7
unsigned char buf[0] = 0xe7;   // e7


// 向上取整数
#include <math.h>
double a = 0.1;
int64_t b = ceil(a);   // 1
