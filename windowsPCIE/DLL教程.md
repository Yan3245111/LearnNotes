# 使用python读取DLL/LIB  动态链接库或者静态链接库
* 正常可以直接使用ctypes 读取dll正常访问寄存器读写，使用vs交叉编译 dumpbin /exports your_lib or your dll 可以看到库里面的函数封装
* h文件（函数声明，需要和DLL/LIB定义的函数一致），一般都由官方提供

# 非正常版，由于只有遗留下来的2个h文件和DLL+LIB，在同目录依赖文件夹下
* python无法正常调用，使用vs 交叉编译获取的函数封装里面有乱码，如下：0 00001030 ??0ComuPCIe@@QEAA@AEBV0@@Z
* 无法知道里面正常参数，就算按照h文件里的参数传递，也直接报错，无法正常调用，所以在现有基础重新封装一层，生成DLL

# 非正常版教程
* 使用QT新建library c++库，选择文件路径，更改文件工程名
* 在.pro添加DLL和LIB的引用路径
  * INCLUDEPATH += $$PWD/PCIEDLL/include  # 假设头文件放在 include 目录
  * LIBS += -L$$PWD/PCIEDLL/lib -lComuPCIe  # name_of_lib 不带前缀和后缀
* 如果找不到默认vs依赖库，也可以手动添加
  * INCLUDEPATH += "C:/Program Files (x86)/Windows Kits/10/Include/10.0.17763.0/ucrt/x64"
  * LIBS += -L"C:/Program Files (x86)/Windows Kits/10/Lib/10.0.17763.0/ucrt/x64"
* 如果是 MSVC 编译器，链接 .lib 文件
  * win32:CONFIG(release, debug|release): LIBS += -L$$PWD/lib -ComuPCIe
  * win32:CONFIG(debug, debug|release): LIBS += -L$$PWD/lib -ComuPCIe
* 添加新建文件的路径，一般自动生成
  * SOURCES += \
          pcielib.cpp

  * HEADERS += \
          pcielib.h \
          pcielib_global.h 
* 然后pcielib.h和cpp文件重新声明定义函数，示例在新h和cpp文件夹下面，声明和定义需要和依赖里h文件的函数加参数一致
* 点击bulid编译，在build/debug里找到生成的dll和lib，使用vs交叉编译重新抓取看里面的函数是否正常
* 把生成的dll和依赖的dll放到同文件目录下，因为新dll需要依赖之前的dll才可以正常通信
* 测试：使用CPID_DLL通信.py 测试打开关闭板子和寄存器读写
* 测试2：使用DLL通信完成测试用例.py 测试DMA等
