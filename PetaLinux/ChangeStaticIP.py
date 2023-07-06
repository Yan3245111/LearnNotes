# 使用命令行执行以下代码即可 需要重新连接，一次性的，reboot之后就没了
# ifconfig eth0 192.168.1.11 netmask 255.255.255.0 up

# 修改时间cmd 也是一次性的 烦人
# date -s 2015-09-08 13:36:00
# date --set 2023-07-04
# date --set 13:36

# shell指令修改
# system(cmd)

#include <unistd.h>
#include <stdio.h>

"""
#include <unistd.h>
#include <stdio.h>


int main(int argc, char *argv[])
{
    char *args[] = {"ls", "-al", "/etc/passwd"};

    if(vfork() == 0)
    {
        execv("/bin/ls", args);
    }
    else
    {
        printf("This is the parent process\n");
    }
    return 0;
}
"""
