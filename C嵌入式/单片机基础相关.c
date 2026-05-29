#include <stdio.h>
#include <stdint.h>

/*--------------- GPIO通用输入输出 ---------------*/
/*
输入模式：
浮空输入：没有上下拉，完全由外部控制，应用于外部有上下拉电阻
上拉输入：内部连接上拉电阻，上拉约40欧，无外部信号时为高点评，应用按键检测，按下接地，松开接VCC
下拉输入：内部连接下拉电阻，无外部信号时为低电平，应用按键检测，按下接VCC，松开接地
模拟输入：输入引脚连接到ADC，应用于模拟信号采集

输出模式：
推挽输出：输出引脚可以驱动高电平和低电平，适用于大多数应用，LED，数字信号控制等
开漏输出：只能输出低电平，高电平靠外部上拉，一般用于I2C总线等需要多设备共享信号线的场合
复用推挽：推挽输出，控制信号由外设控制，应用于外设功能，如UART，SPI等
复用开漏：开漏输出，控制信号由外设控制，应用于外设功能，如I2C等

GPIO速度可选，速度越快，上升/下降时间越短，但是功耗和EMI(电磁干扰)越大，选择合适的速度可以平衡性能和稳定性。
时间=1s / 频率，频率越高，时间越短，速度越快，功耗和EMI越大，比如设置速度为20MHz，那么上升/下降时间约为 1 / 20e6 * 1e9 = 50ns
*/

/*--------------- 定时器 ---------------*/
/*
定时器是一个计数器，当计数值达到预设时，可以触发中断或者其他事件
定时器的计数频率由时钟源决定，常见的时钟源有内部时钟、外部时钟和APB总线时钟
基本工作原理：
时钟源 → 预分频器(PSC) → 计数器(CNT) → 比较器 → 输出/中断
                              ↓
                        自动重载寄存器(ARR)到达后，计数器归零
计数频率 = 时钟频率 / (预分频系数 + 1)  +1是因为分频系数从0开始的
定时时间 = (自动重载值 + 1) / 计数频率
举例：分频系数=11 时钟72MHz， 技术频率=72MHz / (11 + 1) = 6MHz，定时时间=(59999 + 1) / 6MHz = 10ms
想要10ms中断一次，就是0.01s * 6MHz = 60000，所以ARR=59999

一般都有通用的时钟分频
比如外部晶振HSE=8MHz, PLL倍频选择9，得到系统时钟72MHz，AHB不分频=72MHz, APB2不分频=72MHz APB1分频2=36Mhz  APB1定时器自动x2=72MHz
APB2: 挂载GPIO USART1 SPI1 TIM1/TIM8  APB1: 挂载USART2/3 SPI2/3 TIM2/TIM5/TIM6/TIM7 IC2
*/

// 配置TIM2为1ms定时中断

void TIM2_Init(void) {
    // 假设系统时钟72MHz
    // 预分频：7200-1 → 72MHz/7200 = 10KHz
    // 自动重载：10-1 → 10KHz/10 = 1KHz = 1ms
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 7200 - 1;     // 预分频系数
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;  // 向上计数
    htim2.Init.Period = 10 - 1;          // 自动重载值
    htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    HAL_TIM_Base_Init(&htim2);
    
    // 使能中断
    HAL_TIM_Base_Start_IT(&htim2);
}

// 中断回调函数
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {
    if(htim->Instance == TIM2) {
        // 每1ms执行一次
        systick_ms++;  // 全局毫秒计数器
        
        // 可以添加LED翻转、按键扫描等周期性任务
        if(systick_ms % 1000 == 0) {
            HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
        }
    }
}


/*--------------- PWM（脉冲宽度调制）模式 ---------------*/
/*
通过改变高电平占整个周期的比例来控制有效输出 应用LED调光 舵机控制 DAC模拟输出
周期=T 占空比=高电平时间/T
*/

// 假设需要产生1KHz PWM，50%占空比
// 频率 = 72MHz / (PSC+1) / (ARR+1) = 1KHz
// 占空比 = (CCR+1) / (ARR+1) = 50%

void PWM_Init(void) {
    // 1. 配置定时器
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 720 - 1;      // 72MHz/720 = 100KHz
    htim2.Init.Period = 100 - 1;         // 100KHz/100 = 1KHz
    HAL_TIM_PWM_Init(&htim2);
    
    // 2. 配置PWM通道
    TIM_OC_InitTypeDef sConfigOC = {0};
    sConfigOC.OCMode = TIM_OCMODE_PWM1;   // PWM模式1
    sConfigOC.Pulse = 50 - 1;             // 占空比：50/100 = 50%
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    HAL_TIM_PWM_ConfigChannel(&htim2, &sConfigOC, TIM_CHANNEL_1);
    
    // 3. 启动PWM
    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);
}

// 动态改变占空比
void Set_PWM_Duty(uint8_t percent) {
    uint32_t pulse = (percent * (100 - 1)) / 100;
    __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, pulse);
}

/*--------------- 中断请求 ---------------*/
/*
NVIC: 数字越小，优先级越高
抢占优先级：当多个中断同时发生时，优先级高的中断会抢占优先级低的中断
子优先级：当多个同优先级的中断同时发生时，才比较子优先级
Group分类
Group0: 4位抢占，0-15（16级）子优先级0位，0（1级）比较抢占优先级
Group1：3位抢占，0-7（8级）子优先级1位，0-1（2级）比较抢占优先级，子优先级
Group2: 2位抢占，0-3（4级）子优先级2位，0-3（4级）比较抢占优先级，子优先级 最常用
Group3: 1位抢占，0-1（2级）子优先级3位，0-7（8级）比较抢占优先级，子优先级
Group4: 0位抢占，0级（1级）子优先级4位，0-15（16级）比较子优先级
*/
// 中断优先级分组
void HAL_NVIC_SetPriorityGrouping(uint32_t PriorityGroup);

// 分组方式（ARM Cortex-M）：
// Group 0：4位抢占，0位子优先级（16级抢占，1级子）
// Group 1：3位抢占，1位子（8级抢占，2级子）
// Group 2：2位抢占，2位子（4级抢占，4级子）
// Group 3：1位抢占，3位子（2级抢占，8级子）
// Group 4：0位抢占，4位子（1级抢占，16级子）

// 使能中断
void HAL_NVIC_EnableIRQ(IRQn_Type IRQn);

// 设置优先级
void HAL_NVIC_SetPriority(IRQn_Type IRQn, uint32_t PreemptPriority, uint32_t SubPriority);

// 配置示例
void Interrupt_Config(void) {
    // 1. 设置优先级分组（整个系统只需设置一次）
    HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_2);  // 2位抢占，2位子
    
    // 2. 使能串口中断并设置优先级
    HAL_NVIC_SetPriority(USART1_IRQn, 2, 1);   // 抢占2，子1
    HAL_NVIC_EnableIRQ(USART1_IRQn);
    
    // 3. 使能外部中断
    HAL_NVIC_SetPriority(EXTI0_IRQn, 1, 0);    // 抢占1，子0（优先级更高）
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);
}
// 注意1：中断里不能放delay，因为中断服务程序应该尽快执行完毕，delay会阻塞CPU，导致其他中断无法响应，甚至引起系统死锁。中断服务程序应该只处理必要的任务，并尽快返回主程序。
// 注意2：要先开启中断，然后设置标志位，数据解析要放到主循环或者freeRTOS里

/* --------------- 硬错误（HardFault） ---------------*/
/*
常见原因
1. 访问非法地址：如访问未分配的内存、外设寄存器等
2. 栈溢出：函数调用过深，局部变量过多，导致栈空间不足
3. 代码执行错误：如执行了无效指令、跳转到错误的地址等，除以0这种
4. 非对其访问：访问未对齐的内存地址，如32位访问必须4字节对齐，16位访问必须2字节对齐，某些Cortex-M不支持
*/


/* --------------- UART（异步串口） USART才有同步 --------------- */
// 异步：使用波特率同步，不需要时钟线
// 同步：必须使用ck时钟线，靠时钟边沿采样，高速、高精度时才用
/*
数据帧格式：
空闲状态：线保持高电平(RX/TX相同)
起始位：1位，低电平，表示数据帧开始
数据位：通常8bit，实际数据内容，LSB先发送
校验位：可选，奇偶校验，错误检测
停止位：1-2位，高电平，表示数据帧结束
空闲状态：线保持高电平

一个数据最多发255，转换为二进制，然后按位发送，比如255=0b11111111，先发送LSB 1，再发送1，直到最后一个1，最后发送停止位
超过255需要分多次发送，比如1000=0b1111101000，先发送LSB 0，再发送0，直到最后一个1，最后发送停止位
先发低位再发高位，从右往左发，第一位是0位比如0b00000001, 先发1 0 0 0 0 0 0 0，最后发停止位
*/

/* --------------- I2C ---------------*/ 