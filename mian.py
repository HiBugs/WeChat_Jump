# !/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Bob'
import os
import PIL
import numpy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import random

need_update = True


def get_screen_image():
    os.system('adb shell screencap -p /sdcard/screen.png')  # 获取当前界面的手机截图
    os.system('adb pull /sdcard/screen.png')    # 下载当前这个截图到当前电脑当前文件夹下
    return numpy.array(PIL.Image.open('screen.png'))


def jump_to_next(point1, point2):   # 计算距离
    phone = 2
    x1, y1 = point1; x2, y2 = point2
    distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
    press = random.randint(100, 400)
    strs = 'adb shell input swipe ' + (str(press)+' ') * 4 + '{}'
    os.system(strs.format(int(distance * phone)))
   # os.system('adb shell input swipe 320 410 320 410 {}'.format(int(distance*2)))


def on_calck(event, coor=[]):   # 绑定的鼠标单击事件
    global need_update
    coor.append((event.xdata, event.ydata))
    if len(coor) == 2:
        jump_to_next(coor.pop(), coor.pop())
    need_update = True


def update_screen(frame):   # 更新图片
    global need_update
    if need_update:
        time.sleep(1)
        axes_image.set_array(get_screen_image())
        need_update = False
    return axes_image,


figure = plt.figure("Bob's Python Application")   # 创建一张图片
plt.title("WeChat_Jump")
axes_image = plt.imshow(get_screen_image(), animated=True)
plt.axis('off')
figure.canvas.mpl_connect('button_press_event', on_calck)
ani = FuncAnimation(figure, update_screen, interval=50, blit=True)
plt.show()