
a = 2e14 + 10
print(float(a/10000))
'''
4. 在做一个项目时，用到了正点原子的usmart组件
编译时候报错....\OBJ\LED.axf: Error: L6915E: Library reports error: __use_no_semihosting was requested, but _sys_o

在usart.c文件的

_sys_exit(int x) 
{ 
    x = x; 
} 

大约47行后面加入

//__use_no_semihosting was requested, but _ttywrch was 
void _ttywrch(int ch)
{
        ch = ch;
}
https://blog.csdn.net/liu8xu88/article/details/120975004

'''
