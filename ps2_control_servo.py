import time
from machine import Pin, ADC
from libs.servo import Servo

ps2_x = ADC(Pin(32), atten=ADC.ATTN_11DB)
ps2_y = ADC(Pin(33), atten=ADC.ATTN_11DB)
servo_x = Servo(Pin(13), max_us=2500, angle=180)
servo_y = Servo(Pin(12), max_us=2500, angle=180)


def lerp(a, b, t) -> int:
    return int(a + (b - a) * t)


while True:
    # x,y的取值是[-1,1]
    x = ps2_x.read() / 4095  # [0,1]
    y = ps2_y.read() / 4095  # [0,1]

    # 将x从[0,1]映射到[0,10]
    x10 = int(x * 10)
    y10 = int(y * 10)

    # 将x,y的值转换为角度
    x_angle = 180 - 18 * x10
    y_angle = 18 * y10

    # print(f'x:{x10} y:{y10} x_angle:{x_angle} y_angle:{y_angle}')

    servo_x.write_angle(x_angle)
    servo_y.write_angle(y_angle)

    time.sleep(0.1)
