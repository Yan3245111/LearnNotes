import matplotlib.pyplot as plt
import numpy as np

# 解决中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ======================
# 1. PID 控制器 实际应用的时候直接把PID设置给电机就可以了，下面两个类是模拟看pid计算的结果和实际一不一样用的，调试PID用
# ======================
class JointPositionPID:
    def __init__(self, Kp=12, Ki=2, Kd=1.0, dt=0.02):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.integral = 0
        self.prev_error = 0

    def compute(self, target_pos, current_pos):
        error = target_pos - current_pos
        P = self.Kp * error
        self.integral += error * self.dt
        I = self.Ki * self.integral
        D = self.Kd * (error - self.prev_error) / self.dt
        output = P + I + D
        self.prev_error = error
        return np.clip(output, -255, 255)

# ======================
# 2. 梯形速度规划（核心！）
# ======================
class TrapezoidalTrajectory:
    def __init__(self, start_pos, end_pos, max_vel, max_acc, dt=0.02):
        self.start = start_pos
        self.end = end_pos
        self.vel = max_vel
        self.acc = max_acc
        self.dt = dt

        # 计算梯形三段时间
        self.t_acc = max_vel / max_acc
        self.pos_acc = 0.5 * max_acc * self.t_acc**2  # 移动距离=1/2 * acc * t的平方
        self.total_dist = end_pos - start_pos
        self.pos_const = self.total_dist - 2 * self.pos_acc

        if self.pos_const < 0:
            self.pos_const = 0
            self.t_acc = np.sqrt(self.total_dist / max_acc)

        self.t_const = self.pos_const / max_vel
        self.total_time = self.t_acc * 2 + self.t_const

    def get_target(self, t):
        if t < self.t_acc:
            # 加速段
            pos = 0.5 * self.acc * t**2
            vel = self.acc * t
        elif t < self.t_acc + self.t_const:
            # 匀速段
            pos = self.pos_acc + self.vel * (t - self.t_acc)
            vel = self.vel
        elif t < self.total_time:
            # 减速段
            t_dec = t - self.t_acc - self.t_const
            pos = self.pos_acc + self.pos_const + (self.vel * t_dec - 0.5 * self.acc * t_dec**2)
            vel = self.vel - self.acc * t_dec
        else:
            pos = self.end
            vel = 0
        return self.start + pos, vel

# ======================
# 3. 完整仿真（工业流程）
# ======================
def simulate_industrial_robot():
    dt = 0.02
    pid = JointPositionPID(Kp=10, Ki=1.8, Kd=0.8, dt=dt)

    # ========== 你要的参数 ==========
    start_pos = 0
    target_pos = 100
    max_vel = 15
    max_acc = 12
    # ================================

    traj = TrapezoidalTrajectory(start_pos, target_pos, max_vel, max_acc, dt)

    # 状态
    current_pos = 0
    current_vel = 0

    # 记录画图
    t_list = []
    target_list = []
    actual_list = []
    vel_list = []

    t = 0
    for i in range(int(traj.total_time / dt) + 30):
        # ========== 1. 轨迹规划给出实时目标 ==========
        target_p, target_v = traj.get_target(t)

        # ========== 2. PID 计算扭矩 ==========
        torque = pid.compute(target_p, current_pos)

        # ========== 3. 物理模型 ==========
        acc = (torque - 0.6 * current_vel - 0.1 * current_pos) / 0.5
        current_vel += acc * dt
        current_pos += current_vel * dt

        # 记录
        t_list.append(t)
        target_list.append(target_p)
        actual_list.append(current_pos)
        vel_list.append(current_vel)
        t += dt

    # 画图
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 1, 1)
    plt.plot(t_list, target_list, 'r--', label='目标角度（轨迹规划）')
    plt.plot(t_list, actual_list, 'b', label='实际角度（PID跟踪）')
    plt.xlabel('时间(s)')
    plt.ylabel('角度(°)')
    plt.title('工业机械臂：梯形速度规划 + PID 闭环控制')
    plt.legend()
    plt.grid(True)
    plt.show()

simulate_industrial_robot()