# 问题1：无法打开包括文件stddef.h no such file or dictionary
"""
原因：编译器太多了，找不到正确编译器
解决：
1-重新安装vscode并选择sdk windows10插件，2017编译器依赖等
2-重新安装qt，选择2017 2015 编译器
3-打开控制面板-程序卸载：搜索Microsoft c++ package 全部卸载
4-打开系统环境-高级环境-系统环境：添加两个环境  
    * INCLUDE  变量 C:/Program Files (x86)/Windows Kits/10/Include/10.0.17763.0/ucrt
                    C:/Program Files (x86)/Windows Kits/10/Include/10.0.17763.0/shared
                    C:/Program Files (x86)/Windows Kits/10/Include/10.0.17763.0/um
                    C:/Program Files (x86)/Windows Kits/10/Include/10.0.17763.0/winrt
    * LIB      变量 C:/Program Files (x86)/Windows Kits/10/Lib/10.0.17763.0/ucrt
                    C:/Program Files (x86)/Windows Kits/10/Lib/10.0.17763.0/um
"""

# 问题2：无法打开文件ucrtd.lib qt
"""
原因：找不到依赖lib
解决：
在qt pro里添加如下即可

INCLUDEPATH += "C:/Program Files (x86)/Windows Kits/10/Include/10.0.17763.0/ucrt/x64"
LIBS += -L"C:/Program Files (x86)/Windows Kits/10/Lib/10.0.17763.0/ucrt/x64"

"""

# 问题3：无法打开终端查看printf
"""
解决办法：
在qt pro里添加 即可
CONFIG += c++11 console
"""