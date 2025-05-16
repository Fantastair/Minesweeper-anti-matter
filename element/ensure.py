import sys
import pickle
import pygame

import fantas
from fantas import uimanager
u = uimanager
import style

import element.music_play as music_play


class QuitButtonWidget1(fantas.ColorButtonMouseWidget):
	def mousein(self):
		super().mousein()
		quit_title.text = '不   要   啊    ！   ！   ！'
		quit_title.update_img()
		shake_title.launch('continue', start=640)

	def mouseout(self):
		super().mouseout()
		if yes_text.text == '是的 ！':
			quit_title.text = '真   的   要   退   出   吗   ？'
		else:
			quit_title.text = '游    戏    已    暂    停'
		quit_title.update_img()
		shake_title.stop()
		quit_title.rect.centerx = 640

class QuitButtonWidget2(fantas.ColorButtonMouseWidget):
	def mousein(self):
		super().mousein()
		quit_title.text = '没   错  ！    点   这   个  ！'
		quit_title.update_img()

	def mouseout(self):
		super().mouseout()
		if yes_text.text == '是的 ！':
			quit_title.text = '真   的   要   退   出   吗   ？'
		else:
			quit_title.text = '游    戏    已    暂    停'
		quit_title.update_img()

oc = pygame.Color(u.color['BGBLACK'])
oc.a = 0
ac = pygame.Color(u.color['BGBLACK'])
ac.a = 224
quit_bg_cover = fantas.Label(u.size, bg=oc, bd=15, sc=u.color['QUITRED'])
alpha_qbc = fantas.LabelKeyFrame(quit_bg_cover, 'bg', ac, 15, u.harmonic_curve)
bd_qbc = fantas.LabelKeyFrame(quit_bg_cover, 'bd', 15, 15, u.harmonic_curve)

quit_title = fantas.Text('真   的   要   退   出   吗   ？', u.font['douyu'], style.quit_title, center=(640,300))
quit_ensure_button = fantas.SmoothColorButton((150,80), style.quit_ensure_button, bd=2, mousewidget=QuitButtonWidget1, radius={'border_radius': 16}, center=(740,400))
yes_text = fantas.Text('是的 ！', u.font['douyu'], style.quit_text, center=(75,40))
yes_text.join(quit_ensure_button)
quit_ensure_button.bind_shortcut('Return')
shake_title = fantas.RectKeyFrame(quit_title, 'centerx', 660, 10, u.sin_curve)
shake_title.bind_endupwith(shake_title.launch, start=640)

quit_cancel_button = fantas.SmoothColorButton((150,80), style.quit_cancel_button, bd=2, mousewidget=QuitButtonWidget2, radius={'border_radius': 16}, center=(540,400))
style.quit_text['fgcolor'] = u.color['TEXTWHITE']
think_text = fantas.Text('再想想', u.font['douyu'], style.quit_text, center=(75,40))
think_text.join(quit_cancel_button)
quit_cancel_button.bind_shortcut('Escape')
prevent_look = fantas.Label((0,0), bg=u.color['TEXTGRAY'])

def ensure_quit(bg, origin_bg):
	global bg_temp
	if yes_text.text != '是的 ！':
		quit_title.text = '真   的   要   退   出   吗   ？'
		quit_title.update_img()
		yes_text.text = '是的 ！'
		yes_text.update_img()
		think_text.text = '再想想'
		think_text.update_img()
	if map_box.started:
		prevent_look.set_size((map_box.rect.w+5,map_box.rect.h+5))
		prevent_look.rect.topleft = map_box.rect.topleft
		prevent_look.join(bg)
	quit_bg_cover.join(bg)
	quit_ensure_button.join(bg)
	quit_cancel_button.join(bg)
	quit_title.join(bg)
	bg_temp = origin_bg
	u.root = bg
	alpha_qbc.bind_endupwith(None)
	bd_qbc.bind_endupwith(None)
	alpha_qbc.value = ac
	bd_qbc.value = 15
	alpha_qbc.launch(start=oc)
	bd_qbc.launch(start=0)

def quit():
	fantas.dump(u.userdata, 'userdata')
	pygame.quit()
	sys.exit()
quit_ensure_button.bind(quit)

def cancel_quit():
	if not prevent_look.is_root():
		prevent_look.leave()
	quit_ensure_button.leave()
	quit_cancel_button.leave()
	quit_cancel_button.mousewidget.mouseout()
	quit_title.leave()
	alpha_qbc.value = oc
	bd_qbc.value = 0
	alpha_qbc.bind_endupwith(quit_bg_cover.leave)
	bd_qbc.bind_endupwith(set_root, bg_temp)
	alpha_qbc.launch(start=ac)
	bd_qbc.launch(start=15)
	if map_box.started:
		time_ticker.launch('continue')
	music_play.unpause_music()
quit_cancel_button.bind(cancel_quit)

def set_root(root):
	u.root = root

def requit():
	shake_title.bind_endupwith(shake_title.bind_endupwith, shake_title.launch, start=640)
	shake_title.launch(start=640)


def leave(bg, origin_bg):
	global bg_temp
	if yes_text.text != '立即退出':
		quit_title.text = '游    戏    已    暂    停'
		quit_title.update_img()
		yes_text.text = '立即退出'
		yes_text.update_img()
		think_text.text = '回到游戏'
		think_text.update_img()
	if map_box.started:
		prevent_look.set_size((map_box.rect.w+5,map_box.rect.h+5))
		prevent_look.rect.topleft = map_box.rect.topleft
		prevent_look.join(bg)
	quit_bg_cover.join(bg)
	quit_ensure_button.join(bg)
	quit_cancel_button.join(bg)
	quit_title.join(bg)
	bg_temp = origin_bg
	u.root = bg
	alpha_qbc.bind_endupwith(None)
	bd_qbc.bind_endupwith(None)
	alpha_qbc.value = ac
	bd_qbc.value = 15
	alpha_qbc.launch(start=oc)
	bd_qbc.launch(start=0)
