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


// 错误示例 p是野指针
int *p1 = 1;
int *p;
*p = *p1;
// 正确示例
int p;
p = *p1;

// float  不可用 float var == 0 做比较，因为精度不准确，应该设法转换使用>= 或者 <=
float a = 0.1
bool b;
int c;
char *d;
// 一般逻辑判断使用 if(!b)
// 数字判断使用 if(c == 0)
// 指针使用 if(d == NULL)

// char a[100] 作为参数传入函数时，只有char指针属性，使用sizeof(a) 64位操作系统就是8位 32位则是4位 单独使用就是100
