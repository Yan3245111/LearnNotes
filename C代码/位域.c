// 在 struct 结构体中，使用 : 指定变量占用的位数

struct BitField {
    unsigned int a : 3;  // 3 位
    unsigned int b : 5;  // 5 位
    unsigned int c : 2;  // 2 位
} BitField;


typedef struct Register {
    int a;
    int b;
    int c;
} Register;


// 加不加typedef知识写法的区别：不加typedef 声明必须加struct，加了以后代码更简洁
struct BitField bit_field;

Register reg;

/*
变量类型必须是整型（int, unsigned int, char, short）
:3, :5, :2 指定占用的二进制位数
多个位域变量共用同一个 int 变量的存储空间
好处：节省空间，提高代码可读性，不可使用sizeof计算大小，也不能超过int位数
* /
