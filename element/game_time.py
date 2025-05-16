import time

import fantas
from fantas import uimanager
u = uimanager
import style


def show_nowtime():
	global t, last_min
	t = time.localtime()
	if t.tm_min != last_min:
		clock_time.set_part_time(t.tm_hour, t.tm_min)
		last_min = t.tm_min

def show_gametime():
	xjump_clock.launch()
	yjump_clock.launch()
	clear_time.launch()
	if u.show_messages:
		localtime_tip1.cancel_event()
		localtime_tip2.cancel_event()
		gametime_tip1.apply_event()
		gametime_tip2.apply_event()


last_min = time.localtime().tm_min - 1
clock_icontext = fantas.Text(chr(0xe904), u.font['iconfont'], style.clock_icontext, center=(420,130))
clock_time = fantas.TimeText('::', u.font['shuhei'], style.clock_text, bottomleft=(450,145))
clear_time = fantas.TimeTextKeyFrame(clock_time, 'time', 0, 180, u.curve)
clock_time.anchor = 'bottomleft'
time_ticker = fantas.TimeTicker(clock_time)
show_nowtime()

yjump_curve = fantas.FormulaCurve('-4*x**2+4*x')
yjump_clock = fantas.UiSizeKeyFrame(clock_icontext, 'y', (60, 60), 90, yjump_curve)
xjump_curve = fantas.FormulaCurve('4*x**2-4*x-(867*math.cos(4*math.pi*x)-867)/1000')
xjump_clock = fantas.UiSizeKeyFrame(clock_icontext, 'x', (0, 0), 90, xjump_curve)


if u.show_messages:
	localtime_tip1 = fantas.HoverMessage(clock_time, '当前时间', u.hovermessagebox)
	localtime_tip2 = fantas.HoverMessage(clock_icontext, '当前时间', u.hovermessagebox)
	gametime_tip1 = fantas.HoverMessage(clock_time, '游戏时间', u.hovermessagebox)
	gametime_tip2 = fantas.HoverMessage(clock_icontext, '游戏时间', u.hovermessagebox)
	localtime_tip1.apply_event()
	localtime_tip2.apply_event()


def place_element(father):
	clock_icontext.join(father)
	clock_time.join(father)
