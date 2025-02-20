freq_digit = [9, 6, 3, 0]

unit_digit = {0: [9, 6, 3, 0], 1: [1], 2: [9, 6, 3, 0]}


"""
都是最小单位 hz, 先判断单位，然后决定在哪里补0加空格和小数点
1-GHz： 例value=1hz, 长度够不够9，不够往前补0，补够9位，然后加0.，如果长度够9，则从后往前每隔3位补空格，最后一位补小数点
2-MHz  
3-KHz
4_Hz
"""


def value_to_text(value: int, unit: int, param_type: int) -> str:
    is_negative = False if value > 0 else True
    value = abs(value)
    v_len = len(str(value))
    if v_len <= unit_digit[param_type][unit]:
        number_str = str(value).zfill(unit_digit[param_type][unit] + 1)
    else:
        number_str = str(value)
    front_part = number_str[:-unit_digit[param_type][unit]]
    back_part = number_str[-unit_digit[param_type][unit]:]
    formatted_back = " ".join([back_part[max(i - 3, 0):i] for i in range(len(back_part), 0, -3)][::-1])
    formatted_front = " ".join([front_part[max(i - 3, 0):i] for i in range(len(front_part), 0, -3)][::-1])
    res = formatted_back
    if front_part:
        res = f"{formatted_front}.{formatted_back}".strip()
    if is_negative:
        res = '-' + res
    print(res)
    return res


# value_to_text(value=10, unit=0, param_type=0)


"""
原则：正常 text去除空格和小数点即为最小数值， 但是如果直接输入1 或者 0.1去除以后都是1，则要根据当前type转换成最小值，然后发出去
直接进行大小比较，然后传入value_to_text， 再显示到界面即可
"""


def text_to_value(text: str, unit: int, param_type: int) -> tuple:
    res = text.replace(" ", "")
    value = float(res) * 1e9
    print(value)
    return int(value), res.replace(".", "")


text_to_value(text="1.000 000 000", unit=0, param_type=0)
