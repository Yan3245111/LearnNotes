* 1-打开QT工程，在运行上面debug更改为release，重新构建，ctrl+r
* 2-在项目-构建项目找到release目录，并打开，在release下找到exe文件
* 3-新建空文件夹（英文名）把exe文件粘贴到此文件夹下
* 4-在项目-构建项目-构建环境-找到QTDIR看一下编译版本的QT路径
* 5-在电脑搜索输入qt 找到使用的QT编译器。如图片1.png，中科睿信电脑使用的是Qt 5.12.0 for Desktop (MinGW 7.3.0 64-bit)
* 6-双击此Qt 5.12.0 for Desktop (MinGW 7.3.0 64-bit)，进入终端
* 7-输入 windeployqt exe文件路径。如：windeployqt c:\Desktop\a.exe 回车即构建成功
* 8-在新建文件夹下找到exe文件，双击即可运行Qt界面

* 错误1：如果报错：编译exe文件的时候找不到vs安装路径，需要配置windows电脑的环境变量
* 解决办法：电脑右键->属性->高级系统环境->详情键找不到vs路径.png -> 环境变量 -> 下面系统变量 -> 新建
  * -> 变量名：VCINSTALLDIR 变量值：C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC
  * 找到vs在自己电脑的位置 重启电脑即可

* 错误2：编译好的exe启动时报错，无法找到libfftw3-3.dll文件，从网上下载，然后把libfftw3-3.dll 
  * libfftw3f-3.dll 和 libfftw3l-3.dll 粘贴到文件夹下即可

* 错误3：一定要在release模式下生成exe文件，在debug模式下生成的别人电脑无法打开