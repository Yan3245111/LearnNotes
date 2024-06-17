srcfile := $(wildcard *.c ./Interface/*.c ./Interface/Uart/*.c)
srcfile += $(wildcard ./ParamWork/*.c ./ParamWork/PlControl/*.c)

all: 
	#arm-linux-gnueabihf-gcc -o 2U_analog_source $(srcfile) -lpthread -lrt -lm
	#mv 2U_analog_source ~/nfs_server/2U_analog_source
	gcc -o 2U_analog_source $(srcfile) -lpthread -lrt -lm
	#想在linux下运行, 需要把gcc -o 2U_analog_source $(srcfile) -lpthread -lrt -lm打开, 屏蔽两外两条, 且使用sudo执行
clean:
	rm 2U_signal *.o
