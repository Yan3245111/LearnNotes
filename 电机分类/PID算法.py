import matplotlib.pyplot as plt


# 直流电机 + 编码器
class JointPositionPID:

    def __init__(self, kp, ki, kd, dt=0.02):
        self._kp = kp  # 比例系数
        self._ki = ki  # 积分系数
        self._kd = kd  # 微分系数
        self._dt = dt  # 控制周期 20ms

        self._set_angle = 0  # 目标角度
        self._integral = 0  # 积分累加值
        self._prev_error = 0  # 上一次误差
        self._prev_output = 0  # 上一次输出

        self._out_limit = (-255, 255)  # 输出限制 正负255 对应电机PWM的正反转
        self._integral_limit = (-100, 100)  # 积分限幅

    def set_target(self, angle_deg):
        self._set_angle = angle_deg

    def update(self, current_angle):
        error = self._set_angle - current_angle
        # 比例
        P = self._kp * error
        # 积分
        self._integral += error * self._dt
        self._integral = max(self._integral_limit[0], min(self._integral_limit[1], self._integral))
        I = self._ki * self._integral
        # 微分
        derivative = (error - self._prev_error) / self._dt
        D = self._kd * derivative
        # 结果
        output = P + I + D
        output = max(self._out_limit[0], min(self._out_limit[1], output))
        # 赋值
        self._prev_error = error
        self._prev_output = output
        return output


if __name__ == "__main__":
    def simulate_joint():
        pos_pid = JointPositionPID(kp=1.2, ki=0.3, kd=0.2)
        pos_pid.set_target(90)
        # 模拟数据
        angle = 0
        velocity = 0  # 初始角速度设置为0 角度/s
        angles = []
        times = []

        for i in range(500):
            t = i * 0.02
            # 扭矩
            torque = pos_pid.update(angle)
            # 动力学模型  角加速度(acce) = (扭矩 - 摩擦力 - 重力) / 惯性 核心代码
            acce = (torque - 0.5 * velocity - 0.1 * (angle - 1)) / 0.5
            velocity += acce * 0.02  # 累计速度=之前的速度 + 加速度 * 时间
            angle += velocity * 0.02  # 累计角度=之前的角度 + 速度 * 时间
            angles.append(angle)
            times.append(t)
        # 绘图
        plt.plot(times, angles)
        plt.axhline(y=90, color='r', linestyle='--', label='target 90°')
        plt.xlabel('time(s)')
        plt.ylabel('angle(°)')
        plt.title('motor control')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    simulate_joint()
