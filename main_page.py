import time
import pygame
import random

import fantas
from fantas import uimanager
u = uimanager
import style

import element.game_tip as game_tip
import element.settings as settings
import element.music_play as music_play
import element.ensure as ensure
import element.game_map as game_map
import element.game_time as game_time

bg = fantas.Root(u.color['BGDARKGRAY'])

class Leave(fantas.MouseBase):
	__slots__ = tuple()

	def window_lose_focus(self):
		if ensure.quit_bg_cover.is_root():
			music_play.pause_music()
			ensure.leave(fantas.Ui(u.screen.copy()), bg)
		elif not u.userdata['close_directly']:
			ensure.requit()
		if game_time.time_ticker.is_launched():
			game_time.time_ticker.stop()

	def window_hide(self):
		self.window_lose_focus()

Leave(bg, 1).apply_event()

game_map.place_element(bg)
game_tip.place_element(bg)
music_play.place_element(bg)
settings.place_element(bg)
game_time.place_element(bg)

map_box = game_map.map_box

wander_bomb = fantas.IconText(chr(0xe900), u.font['iconfont'], style.wb_text)
wander_bomb.rect.center = (random.randint(480,800), random.randint(240,560))
wander_bomb.angle = random.randint(0,359)
wander_bomb.join(bg)

startgame_button = fantas.SmoothColorButton((240,80), style.startgame_button, bd=2, radius={'border_radius': 20}, center=(640,400))
startgame_button.join(bg)
startgame_text = fantas.Text('开始游戏', u.font['douyu'], style.startgame_text, center=(120,40))
startgame_text.join(startgame_button)
sgb_alpha_out = fantas.UiKeyFrame(startgame_button, 'alpha', 0, 30, u.curve)
sgb_alpha_out.bind_endupwith(startgame_button.leave)
sgb_size_out = fantas.LabelKeyFrame(startgame_button, 'size', (0,0), 30, u.harmonic_curve)
sgb_size_out.bind_endupwith(startgame_button.set_size, (200,60))


class WanderBomb(fantas.KeyFrame):
	__slots__ = ('speed', 'border', 'angle', 'xlast', 'ylast', 'a')

	def tick(self):
		wander_bomb.mark_update()
		wander_bomb.rect.left += self.speed[0]
		wander_bomb.rect.top += self.speed[1]
		wander_bomb.update_img()
		wander_bomb.update_rect()
		if self.angle:
			wander_bomb.angle += self.angle/30
			self.a = (wander_bomb.angle - 45) % 360
			if self.angle > 0:
				self.angle -= 0.5
			else:
				self.angle += 0.5
		xcrash = wander_bomb.rect.right > self.border.right or wander_bomb.rect.left < self.border.left
		ycrash = wander_bomb.rect.bottom > self.border.bottom or wander_bomb.rect.top < self.border.top
		if not self.xlast and xcrash:
			self.speed[0] = -self.speed[0]
			if 360 > self.a > 270 or 180 > self.a > 90:
				self.angle += 90
			else:
				self.angle -= 90
			self.xlast = True
		elif self.xlast and not xcrash:
			self.xlast = False
		if not self.ylast and ycrash:
			self.speed[1] = -self.speed[1]
			if 360 > self.a > 270 or 180 > self.a > 90:
				self.angle -= 90
			else:
				self.angle += 90
			self.ylast = True
			game_time.show_nowtime()
		elif self.ylast and not ycrash:
			self.ylast = False
		if not wander_bomb.rect.colliderect(map_box.rect):
			wander_bomb.rect.center = (random.randint(480,800), random.randint(240,560))
			wander_bomb.angle = random.randint(0,359)
			wb_wander.speed = [2.5*(-1)**random.randint(0,1), 1*(-1)**random.randint(0,1)]
			wb_wander.a = (wander_bomb.angle - 45) % 360
			wander_bomb.update_rect()
			wb_wander.angle = 0
			wb_wander.xlast = False
			wb_wander.ylast = False


wb_wander = WanderBomb()
wb_wander.border = pygame.Rect(map_box)
wb_wander.angle = 0
wb_wander.xlast = False
wb_wander.ylast = False
wb_wander.a = (wander_bomb.angle - 45) % 360
wb_wander.speed = [2.5*(-1)**random.randint(0,1), 1*(-1)**random.randint(0,1)]

center_bomb = fantas.RectKeyFrame(wander_bomb, 'center', map_box.rect.center, 30, u.harmonic_curve)
angle_bomb = fantas.UiKeyFrame(wander_bomb, 'angle', 0, 30, u.harmonic_curve)
shake_curve = fantas.FormulaCurve('math.sin(8*math.pi*(1-math.cos(math.pi*x)))/8**x')
shake_bomb = fantas.RectKeyFrame(wander_bomb, 'center', (map_box.rect.centerx+50,map_box.rect.centery+50), 120, shake_curve)
small_bomb = fantas.TextKeyFrame(wander_bomb, 'size', 50, 120, u.curve)
red_bomb = fantas.TextKeyFrame(wander_bomb, 'fgcolor', u.color['QUITRED'], 150, uimanager.curve)
center_bomb.bind_endupwith(shake_bomb.launch)
angle_bomb.bind_endupwith(small_bomb.launch)
big_bomb = fantas.TextKeyFrame(wander_bomb, 'size', 400, 15, u.slower_curve)
alpha_out_bomb = fantas.UiKeyFrame(wander_bomb, 'alpha', 0, 15, u.curve)
small_bomb.bind_endupwith(big_bomb.launch)
shake_bomb.bind_endupwith(alpha_out_bomb.launch)

title = fantas.Text('历史最高：', u.font['douyu'], style.record_title, center=(520,64))
title.join(bg)
history_time = fantas.TimeText('::', u.font['douyu'], style.record_title, midleft=(680,64))
history_time.join(bg)
history_time.anchor = 'midleft'
history_time.set_time(0)
change_time = fantas.TimeTextKeyFrame(history_time, 'time', None, 40, u.curve)
map_text = fantas.Text('', u.font['shuhei'], style.map_text, midleft=(540, 130))
map_text.join(bg)
map_text.anchor = 'midleft'
dif_text = fantas.Text('', u.font['shuhei'], style.map_text, midleft=(750, 130))
dif_text.join(bg)
dif_text.anchor = 'midleft'

def show_modeinfo(new=False):
	if new:
		title.text = '新纪录：'
	else:
		title.text = '历史最高：'
	title.update_img()
	map_text.text = f"地图大小：{u.userdata['map_size'][0]}×{u.userdata['map_size'][1]}"
	map_text.update_img()
	dif_text.text = f"难度：{getattr(settings, u.userdata['difficulty']).text}"
	dif_text.update_img()
	change_time.value = u.userdata.get((u.userdata['map_size'], u.userdata['difficulty']), 0)
	if change_time.value:
		if history_time.text == '- - : - -':
			history_time.set_time(0)
		change_time.launch('continue')
	else:
		if change_time.is_launched():
			change_time.stop()
		history_time.text = '- - : - -'
		history_time.update_img()
show_modeinfo()
settings.show_modeinfo = show_modeinfo
game_map.show_modeinfo = show_modeinfo


def start_game():
	show_modeinfo()
	fantas.dump(u.userdata, 'userdata')
	sgb_alpha_out.launch()
	sgb_size_out.launch()
	startgame_button.mousewidget.mouseout()
	wb_wander.stop()
	red_bomb.launch()
	center_bomb.launch()
	wander_bomb.angle = wander_bomb.angle % 360 + 360
	angle_bomb.launch()
	game_time.show_gametime()
	if not game_tip.pull_button.fold:
		game_tip.pull_button.展开or收起()
	if not settings.pull_button.fold:
		settings.pull_button.展开or收起()
	game_tip.pull_button.mousewidget.cancel_event()
	settings.pull_button.mousewidget.cancel_event()
	map_box.start_game()
	music_play.fadeout(2000)
startgame_button.bind(start_game)


wb_up = fantas.RectKeyFrame(wander_bomb, 'centery', 300, 60, u.harmonic_curve)
wb_big = fantas.TextKeyFrame(wander_bomb, 'size', 200, 60, u.harmonic_curve)
delay = fantas.Trigger()
lostwin_text = fantas.Text('', u.font['shuhei'], style.lostwin_text, center=(640,480))

def add_size():
	if style.wb_text['size'] > 300:
		style.wb_text['size'] += 12
	elif style.wb_text['size'] > 200:
		style.wb_text['size'] += 18
	elif style.wb_text['size'] > 100:
		style.wb_text['size'] += 24
	wb_big.launch('continue')
game_map.add_size = add_size

def end_game(winned, bomb, pn):
	if winned:
		c = fantas.CircleLabel(0, bg=u.color['TEXTWHITE'], center=(game_map.map_box.rect.w/2,game_map.map_box.rect.h/2))
		c.join(game_map.map_box)
		game_map.map_box.to_remove.append(c)
		c.alpha = 200
		fantas.LabelKeyFrame(c, 'radius', (game_map.map_box.rect.w**2+game_map.map_box.rect.h**2)**0.5, 128, u.harmonic_curve).launch()
		if bomb is not None:
			bomb.leave()
		wander_bomb.join(bg)
		wander_bomb.move_top()
		wander_bomb.rect.center = game_map.map_box.rect.center
		wander_bomb.alpha = 255
		wander_bomb.angle = 0
		style.wb_text['fgcolor'] = u.color['TEXTGRAY']
		style.wb_text['size'] = 100
		wander_bomb.update_img()
		wb_up.launch()
		wb_big.launch()
		lostwin_text.text = '胜  利'
		style.lostwin_text['fgcolor'] = u.color['TEXTGRAY']
		lostwin_text.update_img()
		delay.launch(200)
		fantas.Trigger().launch(270).bind_endupwith(music_play.play_music, 'background')
	else:
		bomb.leave()
		wander_bomb.join(bg)
		wander_bomb.rect.center = game_map.map_box.rect.center
		wander_bomb.alpha = 255
		wander_bomb.angle = 0
		style.wb_text['fgcolor'] = u.color['TEXTWHITE' if pn else 'TEXTGRAY']
		style.wb_text['size'] = 100
		wander_bomb.update_img()
		wb_up.launch()
		wb_big.launch()
		lostwin_text.text = '失  败'
		style.lostwin_text['fgcolor'] = u.color['TEXTWHITE' if pn else 'TEXTGRAY']
		lostwin_text.update_img()
		delay.launch(90)
		fantas.Trigger().launch(180).bind_endupwith(music_play.play_music, 'background')
game_map.end_game = end_game


def show_playagain():
	if lostwin_text.text == '失  败':
		music_play.play_sound('beat')
	else:
		music_play.play_sound('new_record')
	lostwin_text.join(bg)
	game_map.map_box.to_remove.append(lostwin_text)
	startgame_text.text = '再玩一局'
	startgame_text.style = style.playagain_text
	startgame_text.rect.center = (100,30)
	startgame_text.update_img()
	startgame_button.rect.center = (640,580)
	startgame_button.alpha = 255
	startgame_button.join(bg)
	startgame_button.bind(replay_game)
	game_tip.pull_button.mousewidget.apply_event()
	settings.pull_button.mousewidget.apply_event()
delay.bind_endupwith(show_playagain)


def replay_game():
	game_map.map_box.reset_game()
	start_game()
