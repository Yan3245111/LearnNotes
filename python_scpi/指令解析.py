import re


class SCPIParser:
    def parse(self, command):
        # 正则拆解指令
        match = re.match(r"([\[:\w\]*]+)\s?([\d\.]+)?([a-zA-Z]+)?", command)

        if match:
            cmd = match.group(1)  # 提取命令部分
            value = match.group(2)  # 提取数值
            unit = match.group(3)  # 提取单位
            return self.clean_command(cmd), value, unit
        return None, None, None

    def clean_command(self, cmd):
        """去掉可选的 '[]'，并展开 ':' 符号"""
        cmd = cmd.replace("[", "").replace("]", "")  # 移除可选符号
        cmd_parts = cmd.split(":")  # 按层级分割
        return [part for part in cmd_parts if part]  # 过滤空字符串


# 测试解析器
parser = SCPIParser()
cmd, value, unit = parser.parse("[:SOURce]:FREQuency[:CW] 1GHz")

print(f"解析后的指令路径: {cmd}")  # ['SOURce', 'FREQuency', 'CW']
print(f"解析后的数值: {value}")  # 1
print(f"解析后的单位: {unit}")  # GHz


cmd, value, unit = parser.parse(":OUTPut[:STATe] On")

print(f"解析后的指令路径: {cmd}")  # ['SOURce', 'FREQuency', 'CW']
print(f"解析后的数值: {value}")  # None
print(f"解析后的单位: {unit}")  # Off


cmd, value, unit = parser.parse("[:SOURce]:PULSe:PRI1[:STATe] 1us")

print(f"解析后的指令路径: {cmd}")  # ['SOURce', 'FREQuency', 'CW']
print(f"解析后的数值: {value}")  # None
print(f"解析后的单位: {unit}")  # Off
