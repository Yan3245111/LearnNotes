# TRIGGER MODE

# 连续触发
def free_run_mode():
    int_count = "INITiate:CONTinuous ON"
    trig_source = "TRIGger:SOURce IMMediate"


# 单次触发
def single_shot():
    int_count = "INITiate:CONTinuous OFF"
    trig_source = "TRIGger:SOURce IMMediate"


# 触发模式查询指令：设置完以后设置单次/连续触发，然后再使用read/fetch进行读取 内部连续触发fetch速度最快，4.4ms测量一次
def trigger_mode():
    trigger_source = "TRIGger:SOURce INTERNAL"  # or EXTERNAL
