#include <string.h>
#include <stdio.h>

// 字符串拼接
char buf[100];
char *text = "1234";
memset(buf, 0x00, sizeof(buf))
strcat(buf, text);  // 单字符串拼接

snprintf(buf, sizeof(buf), "%s/%s", text, "567")  // 多字符串拼接

// 字符串比对，包含关系，前面全部包含后面的则p=前面
char *p = strstr("123", "12")
if (p) {

}

// 字符串比对，等于0则str1=str2， 小于0则str1<str2, 大于0则str1>str2， 是按照当前字符串的ascii码排序进行比对的
int res = strcmp("123", "213")
if (res) {

}

// 字符串copy
strcpy(buf, text);  // "1234"，如果之前有数据会被覆盖

//