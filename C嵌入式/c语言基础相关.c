// 指针
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>


/*--------------------- 指针相关 -------------------- */
/*
& 取地址运算符，获取变量的地址
* 解引用运算符，获取指针指向的值
p 是地址，*p是地址里的值
更改*p 即更改地址p指向的值，所有指向这个地址的变量的值都会改变
*/
void set_point(void) {
    int a = 1;
    int *p = &a; // 定义一个指针变量p，指向a的地址
    printf("111 %d %d\n", *p, a); // 通过指针访问a的值
    *p = 2; // 通过指针修改a的值
    printf("222 %d %d\n", *p, a); // 输出a的值，应该是2
}


/*
为什么使用指针
1.函数需要修改参数的值，必须使用指针传递参数，这样在函数内部更改参数，外部的值也会更改
2.避免大数据拷贝，整个结构体拷贝很大，使用结构体的指针只拷贝4/8字节的地址
*/
typedef struct Student
{
    /* data */
    char name[10];
    int age;
} student;

student stu1;

void set_info(student *s) {
    s->age = 10;
    sprintf(s->name, "zhangsan");
}


/*
底层逻辑，指针本身大小是4B（32位系统）或8B（64位系统），无论它指向的数据类型是什么，自身大小不变。指针存储的是一个地址，这个地址指向内存中的某个位置。通过这个地址，我们可以访问或修改该位置的数据。
使用指针赋值数据时，p指向第一个值的地址，p+1 移动的是n * sizeof(数据类型类型)个字节，且指针也可以使用下标
*/
void move_p(void) {
    char str[] = "hello";
    char *p = str; // p指向字符串str的第一个字符的地址
    printf("11111 %c %d\n", *p, sizeof(p)); // 输出h
    p++; // p指向下一个字符的地址
    printf("22222 %c %d\n", *p, sizeof(p)); // 输出e
    // 使用下标
    printf("33333 %c\n", p[3]); // 输出o，因为p++指向了e
}


/*
多级指针，指针存储的地址可以被另一个指针指向
使用函数更改外面的指针的地址时候，需要使用二级指针
*/
void allocate_memroy(int **p) {
    *p = (int *)malloc(sizeof(int)); // 分配内存并将地址赋值给*p
    **p = 42; // 通过二级指针修改分配的内存中的值
}

void two_p(void) {
    int a = 1;
    int *p1 = &a; // p1指向a的地址
    int **p2 = &p1; // p2指向p1的地址
    printf("111 %d %d %d\n", *p1, **p2); // 输出a的值，应该是1
    **p2 = 2; // 通过二级指针修改a的值
    printf("222 %d %d\n", *p1, **p2); // 输出a的值，应该是2
    /*
    a的值1， &a 地址1000 
    p1 a的地址  1000
    *p1 a的地址的值即a的值1
    p2 p1的地址 2000
    *p2 p1的地址 1000
    **p2 p1的地址的值即a的值1
    */
}


/*
函数传递
*/
void set_timer_callback(void (*callback)(int a)) {
    callback(10);
}

void timer_callback(int a) {
    printf("Timer callback called! %d\n", a);
}

void class1(void) {
    set_point();
    set_info(&stu1);
    printf("%d %s\n", stu1.age, stu1.name);
    move_p();
    int *buffer;  // 如果在使用之前不赋值就会变成野指针
    allocate_memroy(&buffer); // 传递buffer的地址，即二级指针
    two_p();
    set_timer_callback(timer_callback);
}

/*--------------------  const相关  --------------------------*/
/*
const修饰普通变量 const告诉编译器 变量不可修改，强行修改会报错
*/
void const_error1(void) {
    const int a = 1;
    // a = 2; // 错误，a是常量，不能修改
}


/*
const修饰指针 看const在*的左边还是右边，在左指内容，在右指本身
 */
void const_error2(void) {
    int num = 10;
    const int *p2 = &num;  // 等同于 int const *p2 = 10;
    // *p2 = 20; // 错误，p2指向的内容是常量，不能修改
    p2 = &num; // 正确，p2是一个指针变量，可以修改指针本身的地址

    int *const p3 = &num; 
    // p3 = 20; // 错误，p3是一个常量指针，不能修改指针本身的地址
    *p3 = 20; // 正确，p3指向的内容是变量，可以修改

    const int *const p4 = &num; // p4是一个常量指针，指向一个常量
    // p4 = 20; // 错误，p4是一个常量指针，不能修改指针本身的地址
    // *p4 = 20; // 错误，p4指向的内容是常量，不能修改
}

/*
static 函数只能在当前文件访问，所以在不同文件可以有同名的函数，可以隐藏实现细节
*/


void class2(void) {
    const_error1();
    const_error2();
}

/*------------------- static相关 ------------------------ */
/* 生命周期从程序启动到结束只初始化一次 */
void count_calls(void) {
    static int count = 0;
    count++;
    printf("called times %d\n", count);
}

void class3(void) {
    count_calls();
    count_calls();
}

/*--------------结构体 联合体 位域--------------*/
/*结构体自动补齐规则
1.成员放在自己的对齐倍数上，比如int是4字节，比如放在4的倍数上，如果前面占用了1字节，那么就会在后面补齐3字节，直到下一个成员的对齐倍数满足要求
2.总倍数必须是最大成员的倍数，比如int是4字节，那么总大小必须是4的倍数，如果前面占用了5字节，那么就会在后面补齐3字节，直到总大小满足要求
3.结构体嵌套，先计算内部结构体大小，再计算外部结构体大小，内部结构体的对齐倍数就是外部结构体的对齐倍数，整体对齐倍数是最大成员的对齐倍数
*/
typedef struct Example1 {
    char a; // 1字节
    int b;  // 4字节
    short c; // 2字节
    /* char a 字节为1 放在地址0上
    int b 字节为4 必须放在4的倍数，所以a要补3字节，放在地址4上，占用4-7
    short c 字节为2，放在2的倍数上，刚好是8，占用8-9
    整体占用：1 + 3（补齐）+ 4 + 2 + 2（补齐）= 12字节，但是应该为最大字节的倍数，即4的倍数，所以还需要补齐2字节
     */
} example1;

typedef struct Example2 {
    int a;  // 4字节
    char b; // 1字节
    short c; // 2字节
    /* int a 字节为4 放在地址0上，占用0-3
    char b 字节为1，放在地址4上
    short c 字节为2，需放在2的倍数，所以b要补齐1字节，放在地址6上，占用6-7
    整体占用：4 + 1 + 1（补齐）+ 2 = 8字节，已经是最大字节的倍数了，不需要再补齐
    */
} example2;

// 结构体嵌套
typedef struct Example3 {
    short a; // 2字节
    int b; // 4字节
} example3;

typedef struct Example4 {
    char c; // 1字节
    example3 e; // 6字节
    /*
    先计算example3，short a 字节为2 放在地址0上，占用0-1
    int b 字节为4，需放在4的倍数，所以a要补齐2字节，放在地址4上，占用4-7
    char c字节为1 放在地址0上，占用0
    example3 e 字节为8，必须放在最大字节倍数上，所以c要补齐3字节，e放在地址4上，占用4-11 整体为12字节
    */
} example4;

// 手动对齐 pack push pop 讲解
#pragma pack(1) // 1字节对齐
struct Test {
    int a;
    char b;
    // 1字节对齐，所以是总字节是5
} test;
#pragma pack()  // 恢复默认对齐 只影响后面的结构体，如果下面重写一个对齐，也没影响

#pragma pack(push, 1)
struct Test1 {
    int a;
    char b;
} test1;
#pragma pack(pop)  // 删除当前对齐，恢复上一次对齐 比如之前设置了一次2，那后面的结构体对齐就是2了
 
void print_struct_size(void) {
    printf("Size of example1: %lu\n", sizeof(example1)); // 输出example1的大小，应该是12字节
    printf("Size of example2: %lu\n", sizeof(example2)); // 输出example2的大小，应该是8字节
    printf("Size of example4: %lu\n", sizeof(example4)); // 输出example4的大小，应该是12字节
    printf("Size of test: %lu\n", sizeof(test));
}

// 联合体 所有成员公用同一块内存，大小等于最大成员的大小
// 因为用的是同一块内存，所以你只需要存一个数据，就可以看到它别的类型的数据，最常用的就是通信解析
union Data {
    char a[4];
    int b;
    // 总大小等于最大int内存大小4字节
};

union Data data1;


void print_union_size(void) {
    data1.b = 0x01020304;
    printf("size of data1: %lu\n", sizeof(data1));
    printf("data 0x%02x%02x %d\n", data1.a[0], data1.a[1], data1.b);  // 小端输出
}

// 位域 位域是结构体的一种特殊成员，可以指定占用的位数，常用于节省内存或者表示一些标志位
// 一般用于硬件寄存器，通信协议，节省内存
struct Flags {
    uint8_t enable: 1;
    uint8_t mode: 2;
    uint8_t status: 3;
    uint8_t reserved: 2; // 保留位，未使用
};

struct Flags flags;
void print_flags_size(void) {
    printf("size of flags: %lu\n", sizeof(flags)); // 输出flags的大小，应该是1字节
    flags.enable = 1;  // 赋值不可超过自己的位数
    flags.mode = 2;
    flags.status = 7;
    printf("flags: enable=%d, mode=%d, status=%d\n", flags.enable, flags.mode, flags.status); // 输出flags的值
}


void class4(void) {
    print_struct_size();
    print_union_size();
    print_flags_size();
}

/* -------------------内存管理-----------------------*/
//内存分为：堆 栈 全局/静态区 常量区 代码区
/*
堆：malloc/free 手动申请释放的空间，生命周期由程序员控制，适合存储大数据或者需要动态调整大小的数据
栈：局部变量，函数里定义的变量 参数，生命周期由函数调用控制，适合存储小数据或者临时数据
全局/静态区：全局变量，静态变量，只初始化一次，生命周期从程序开始到结束，适合存储需要全局访问或者需要保持状态的数据
常量区：字符串常量，const修饰的变量，生命周期从程序开始到结束，适合存储不可修改的数据
代码区：存储编译好的二进制代码，程序执行时从这里加载指令，只读，不可修改

栈自动，堆手动
全局静态一直住
常量只读不能动
代码存的是指令
*/
// 栈溢出：递归调用太多，导致局部变量太大，超过栈的大小，程序崩溃，这样建议使用s全局变量只创建一次，或者创建在堆上
void stack_overflow(void) {
    char buffer[1024]; // 每次调用都会在栈上分配1024字节的空间
    stack_overflow(); // 无限递归调用，导致栈溢出
}

//堆的使用 malloc/free
void heap_example(void) {
    int *p = (int *)malloc(sizeof(int)); // 在堆上分配4字节的空间，返回地址 指向的是内存
    if (p == NULL) {
        printf("Memory allocation failed!\n");
        return;
    }
    *p = 42; // 通过指针访问堆上的内存
    printf("Value: %d\n", *p); // 输出42
    free(p); // 释放堆上的内存
    p = NULL; // 避免悬空指针 必须加，不然如果后面继续使用p，就会访问已经释放的内存，导致不可预知的行为
}


void class5(void) {
    const char *str1 = "hello"; // "hello" → 常量区  str存在栈区，可变
    str1 = "world"; // 正确，str是一个指针变量，可以修改指针本身的地址，修改的是地址
    // *str = "1"; // 错误，str指向的内容是常量，不能修改
    printf("%s\n", str1); // 输出world
}

/*---------------预处理指令-----------*/
// 预处理是问题替换，宏定义是文本替换，编译完就消失，不占用内存
#define pi 3.1415926  // 单纯文本替换，你写什么就是什么，你后面多写，。；什么都行，编译器根本不管，直接替换，然后应用报错
#define MAX(a, b) ((a) > (b) ? (a): (b))

void define_test1(void) {
    printf("pi: %f\n", pi); // 输出pi: 3.141593
    int x = 10, y = 20;
    int max = MAX(x, y); // 替换为 ((x) > (y) ? (x): (y)) 这个时候才会有占用，存放到栈上，编译器会优化掉这个宏定义，直接替换为20
    int max1 = MAX(x++, y++);
    printf("max: %d max1 %d\n", max, max1); // 输出max: 20 max1: 20 因为x++和y++在替换后变成了 ((x++) > (y++) ? (x++): (y++))，所以x和y都被自增了两次，最终x变成了12，y变成了22，结果不可控，可能是20 也可能是21 也可能是22
}

// 宏定义为什么要加括号，因为他是文本替换，具体如下
#define SQUARE(x) x * x

void define_test2(void) {
    int result = SQUARE(5 + 1); // 替换为 5 + 1 * 5 + 1，结果是5 + 1 * 5 + 1 = 11，而不是36，所以需要加括号
    printf("result: %d\n", result); // 输出result: 11
}


void class6(void) {
    define_test1();
    define_test2();
}


int main(void) {
    // class1();
    // class2();
    // class3();
    // class4();
    // class5();
    class6();
    return 0;
}