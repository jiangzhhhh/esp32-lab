import time
import math
from machine import Pin


beep = Pin(15, Pin.OUT)
beep.value(1)

led = Pin(2, Pin.OUT)

# 定义位选线对象
seg_1 = Pin(5, Pin.OUT)
seg_2 = Pin(18, Pin.OUT)
seg_3 = Pin(19, Pin.OUT)
seg_4 = Pin(21, Pin.OUT)

# 定义位选线列表
seg_list = [seg_1, seg_2, seg_3, seg_4]

# 定义段选线对象
a = Pin(32, Pin.OUT)
b = Pin(25, Pin.OUT)
c = Pin(27, Pin.OUT)
d = Pin(12, Pin.OUT)
e = Pin(13, Pin.OUT)
f = Pin(33, Pin.OUT)
g = Pin(26, Pin.OUT)
dp = Pin(14, Pin.OUT)

led_list = [a, b, c, d, e, f, g, dp]

number_dict = {
    #  [a, b, c, d, e, f, g, dp]
    0: [1, 1, 1, 1, 1, 1, 0, 0],
    1: [0, 1, 1, 0, 0, 0, 0, 0],
    2: [1, 1, 0, 1, 1, 0, 1, 0],
    3: [1, 1, 1, 1, 0, 0, 1, 0],
    4: [0, 1, 1, 0, 0, 1, 1, 0],
    5: [1, 0, 1, 1, 0, 1, 1, 0],
    6: [1, 0, 1, 1, 1, 1, 1, 0],
    7: [1, 1, 1, 0, 0, 0, 0, 0],
    8: [1, 1, 1, 1, 1, 1, 1, 0],
    9: [1, 1, 1, 1, 0, 1, 1, 0],
}


def clear():
    for seg in seg_list:
        seg.on()
    for led in led_list:
        led.off()


def display_digit(digit):
    logic_list = number_dict.get(digit)
    for i in range(len(logic_list)):
        led_list[i].value(logic_list[i])


def switch_seg(order):
    for seg_i in range(len(seg_list)):
        seg_list[seg_i].value(0 if seg_i == order else 1)


def clear_led():
    for led in led_list:
        led.off()


def display(number: float, decimal_places: int, max_num_digits: int = 4):
    number = round(number, 1)
    integer = int(number * (10**decimal_places))
    # because we have one more digit for the decimal point
    integer = max(integer, 0)
    integer = min(integer, 10**(max_num_digits-decimal_places) - 1)
    digits = []
    remainder = integer
    for i in range(max_num_digits):
        n = remainder % 10
        digits.append(n)
        remainder //= 10
    digits.reverse()
    valid_order = 0
    for i in range(len(digits)):
        if digits[i] != 0:
            valid_order = i
            break
    for i in range(valid_order, len(digits)):
        digit = digits[i]
        switch_seg(i)
        display_digit(digit)
        if decimal_places > 0 and i == len(digits) - decimal_places - 1:
            dp.value(1)
        time.sleep_ms(5)


def alarm(enable):
    beep.value(0 if enable else 1)
    led.value(1 if enable else 0)


old_time = time.ticks_ms()
last_time = time.ticks_ms()
countdown_seconds = 15
led_time = 0
beep_time = 0
while True:
    now_time = time.ticks_ms()
    delta_time = now_time - last_time
    last_time = now_time

    # display the remaining time every tick
    # when the remaining time is less than 0, reset the old_time
    elapsed_time = time.ticks_diff(now_time, old_time)
    countdown_remaining_ms = countdown_seconds * 1000 - elapsed_time
    countdown_s = countdown_remaining_ms / 1000.0
    if countdown_s <= 0:
        break
    elif countdown_s < 10:
        decimal_places = 1
    else:
        decimal_places = 0
    display(countdown_s, decimal_places)

    # flick the led every 200ms
    led_time += delta_time
    if led_time > 200:
        led_time = 0
        led.value(1 if led.value() == 0 else 0)

    # beep every 500ms
    beep_interval = 500
    if countdown_s < 1:
        beep_interval = 0
        beep.value(0)
    elif countdown_s < 3:
        beep_interval = 50
    elif countdown_s < 10:
        beep_interval = 200
    else:
        beep_interval = 500
    if beep_interval > 0:
        beep_time += delta_time
        if beep_time > beep_interval:
            beep_time = 0
            beep.value(1 if beep.value() == 0 else 0)


led.value(1)
beep.value(0)
for seg in seg_list:
    seg.off()
for l in led_list:
    l.on()
time.sleep_ms(3*1000)

beep.value(1)
led.value(0)
clear()
