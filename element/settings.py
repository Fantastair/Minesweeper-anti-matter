import pygame

import fantas
from fantas import uimanager
u = uimanager
import style

from element.pull_page import PullButton
import element.music_play as music_play


pull_button = PullButton('left', (310,590), (40,120), style.pull_button, bd=2, radius={'border_top_right_radius': 16,'border_bottom_right_radius': 16}, midleft=(0,380))
if u.show_messages:
	pull_button.unfold_tip = fantas.HoverMessage(pull_button, '展开设置面板', u.hovermessagebox)
	pull_button.unfold_tip.apply_event()
	pull_button.fold_tip = fantas.HoverMessage(pull_button, '收起设置面板', u.hovermessagebox)


class SlideBlock(fantas.SlideBlock):
	__slots__ = ('text_light', 'text_dark', 'text_big', 'text_small', 'option', 'content')

	def __init__(self, option, content, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.text_light = fantas.TextKeyFrame(None, 'fgcolor', u.color['BUTTONBDBLUE'], 10, u.curve)
		self.text_dark = fantas.TextKeyFrame(None, 'fgcolor', u.color['TEXTWHITE'], 7, u.curve)
		self.text_big = fantas.TextKeyFrame(None, 'size', 26, 7, u.curve)
		self.text_small = fantas.TextKeyFrame(None, 'size', 19, 7, u.curve)
		self.option = option
		self.content = content

	def choose(self, option):
		music_play.play_sound('click')
		if self.last_option is not None:
			self.text_dark.text = self.text_small.text = self.last_option
			self.text_small.launch('continue')
			self.text_dark.launch('continue')
		self.text_light.text = self.text_big.text = option
		self.text_big.launch('continue')
		self.text_light.launch('continue')
		u.userdata[self.option] = self.content[option.text]
		if show_modeinfo is not None:
			show_modeinfo()

show_modeinfo = None
fantas.Text('地图大小', u.font['shuhei'], style.choose_title, midleft=(30,40)).join(pull_button.page)
map_16x16 = fantas.Text('16 × 16 格', u.font['shuhei'], dict(style.choose_text), midleft=(60,80))
map_16x16.join(pull_button.page)
map_30x16 = fantas.Text('30 × 16 格', u.font['shuhei'], dict(style.choose_text), midleft=(60,110))
map_30x16.join(pull_button.page)

fantas.Label((260,4), bg=u.color['TEXTGRAY'], radius={'border_radius': 2}, center=(155,140)).join(pull_button.page)

choose_map = SlideBlock('map_size', {'16 × 16 格': (16,16), '30 × 16 格': (30,16)}, 'y', (map_16x16, map_30x16), (8,30), bg=u.color['BUTTONBDBLUE'], radius={'border_radius': 4}, midleft=(30,80))
choose_map.join(pull_button.page)
if u.userdata['map_size'] == (16, 16):
	choose_map.choose_(map_16x16)
else:
	choose_map.choose_(map_30x16)

easy = fantas.Text('简单', u.font['shuhei'], dict(style.choose_text), center=(70,180))
medium = fantas.Text('中等', u.font['shuhei'], dict(style.choose_text), center=(155,180))
difficult = fantas.Text('困难', u.font['shuhei'], dict(style.choose_text), center=(240,180))
choose_mode = SlideBlock('difficulty', {'简单': 'easy', '中等': 'medium', '困难': 'difficult'}, 'x', (easy, medium, difficult), (60,8), bg=u.color['BUTTONBDBLUE'], radius={'border_radius': 4}, center=(155,160))
choose_mode.join(pull_button.page)
easy.join(pull_button.page)
medium.join(pull_button.page)
difficult.join(pull_button.page)
if u.userdata['difficulty'] == 'easy':
	choose_mode.choose_(easy)
elif u.userdata['difficulty'] == 'medium':
	choose_mode.choose_(medium)
else:
	choose_mode.choose_(difficult)

fantas.Label((260,4), bg=u.color['TEXTGRAY'], radius={'border_radius': 2}, center=(155,220)).join(pull_button.page)


class ProcessBar(fantas.ProcessBar):
	__slots__ = ('key', 'num', 'temp_volume')

	def __init__(self, key, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.key = key
		self.num = fantas.Text('', u.font['shuhei'], style.processbar_num, center=(self.block.rect.width/2,self.block.rect.height/2))
		self.num.join(self.block)
		self.temp_volume = 0

	def set_data(self, *args, **kwargs):
		super().set_data(*args, **kwargs)
		self.num.text = str(self.data)
		self.num.update_img()
		u.userdata[self.key+'_volume'] = self.data
		getattr(music_play, f'set_{self.key}_volume')(self.data/(self.extent[1]-self.extent[0]))
		if self.get_data() != 0 and music_play.sound_control_button.text == chr(0xe903):
			music_play.unmute(link=False)

	def mute(self):
		self.temp_volume = self.get_data()
		self.set_data(0, set_pos=True)

	def unmute(self):
		if self.temp_volume and self.get_data() == 0:
			self.set_data(self.temp_volume, set_pos=True)


music_play.music_processbar = music_processbar = ProcessBar('music', (0,100), 'x', fantas.Label((24,24),bg=u.color['BUTTONBDBLUE'],bd=2,sc=u.color['TEXTWHITE'], radius={'border_radius': 6}), style.musicset_processbar, (204,12), bd=2, sc=u.color['TEXTWHITE'], radius={'border_radius': 4}, center=(180,260))
music_processbar.join(pull_button.page)
music_processbar.set_data(u.userdata['music_volume'], smooth=False, set_pos=True)
fantas.Text('音量', u.font['shuhei'], style.settings_text1, center=(44,260)).join(pull_button.page)
# fantas.Label(music_processbar.rect.size, bd=music_processbar.bd, sc=music_processbar.sc, radius={'border_radius': 4}, topleft=(0,0)).join_to(music_processbar, 1)

music_play.sound_processbar = sound_processbar = ProcessBar('sound', (0,100), 'x', fantas.Label((24,24),bg=u.color['BUTTONBDBLUE'],bd=2,sc=u.color['TEXTWHITE'], radius={'border_radius': 6}), style.musicset_processbar, (204,12), bd=2, sc=u.color['TEXTWHITE'], radius={'border_radius': 4}, center=(180,300))
sound_processbar.join(pull_button.page)
sound_processbar.set_data(u.userdata['sound_volume'], smooth=False, set_pos=True)
fantas.Text('音效', u.font['shuhei'], style.settings_text1, center=(44,300)).join(pull_button.page)
# fantas.Label(sound_processbar.rect.size, bd=sound_processbar.bd, sc=sound_processbar.sc, radius={'border_radius': 4}, topleft=(0,0)).join_to(sound_processbar, 1)

fantas.Label((260,4), bg=u.color['TEXTGRAY'], radius={'border_radius': 4}, center=(155,330)).join(pull_button.page)

if u.userdata['muted']:
	music_play.mute()

def click_hover(flag):
	if flag:
		color_hover_text.value = u.color['BUTTONBDBLUE']
		color_hover_text.launch('continue')
	else:
		color_hover_text.value = u.color['TEXTWHITE']
		color_hover_text.launch('continue')
	u.userdata['show_hovermessage'] = flag
	music_play.play_sound('click')

def click_skip(flag):
	if flag:
		color_skip_text.value = u.color['BUTTONBDBLUE']
		color_skip_text.launch('continue')
	else:
		color_skip_text.value = u.color['TEXTWHITE']
		color_skip_text.launch('continue')
	u.userdata['skip_startani'] = flag
	music_play.play_sound('click')

def click_direct(flag):
	if flag:
		color_direct_text.value = u.color['BUTTONBDBLUE']
		color_direct_text.launch('continue')
	else:
		color_direct_text.value = u.color['TEXTWHITE']
		color_direct_text.launch('continue')
	u.userdata['close_directly'] = flag
	music_play.play_sound('click')


tb = fantas.TickBox(24, chr(0xe901), u.font['iconfont'], 20, style.tickbox, click_hover, offset=(0,-1), radius={'border_radius': 4}, center=(50,370))
tb.join(pull_button.page)
t = fantas.Text('鼠标悬浮后显示提示', u.font['shuhei'], dict(style.settings_text2), midleft=(80,370))
t.join(pull_button.page)
tb.set_assist_click(t)
color_hover_text = fantas.TextKeyFrame(t, 'fgcolor', None, 15, u.curve)
if u.userdata['show_hovermessage']:
	tb.click()

tb = fantas.TickBox(24, chr(0xe901), u.font['iconfont'], 20, style.tickbox, click_skip, offset=(0,-1), radius={'border_radius': 4}, center=(50,410))
tb.join(pull_button.page)
t = fantas.Text('跳过游戏的启动动画', u.font['shuhei'], dict(style.settings_text2), midleft=(80,410))
t.join(pull_button.page)
tb.set_assist_click(t)
color_skip_text = fantas.TextKeyFrame(t, 'fgcolor', None, 15, u.curve)
if u.userdata['skip_startani']:
	tb.click()

tb = fantas.TickBox(24, chr(0xe901), u.font['iconfont'], 20, style.tickbox, click_direct, offset=(0,-1), radius={'border_radius': 4}, center=(50,450))
tb.join(pull_button.page)
t = fantas.Text('关闭游戏时不再询问', u.font['shuhei'], dict(style.settings_text2), midleft=(80,450))
t.join(pull_button.page)
tb.set_assist_click(t)
color_direct_text = fantas.TextKeyFrame(t, 'fgcolor', None, 15, u.curve)
if u.userdata['close_directly']:
	tb.click()

fantas.Label((260,4), bg=u.color['TEXTGRAY'], radius={'border_radius': 2}, center=(155,490)).join(pull_button.page)

quit_game_button = fantas.SmoothColorButton((180,40), style.quit_ensure_button, bd=2, radius={'border_radius': 12}, center=(155,540))
quit_game_button.join(pull_button.page)
fantas.Text('退出游戏', u.font['shuhei'], style.quit_text_small, center=(90,20)).join(quit_game_button)
quit_game_button.bind(pygame.event.post, pygame.event.Event(pygame.QUIT))

def place_element(father):
	pull_button.join(father)
