import pygame
import threading
from tempfile import TemporaryFile

import fantas
from fantas import uimanager
u = uimanager
import style


sound_control_button = fantas.Text(chr(0xe902), u.font['iconfont'], style.sound_icontext, topright=(1260,20))
scb_widget = fantas.AnyButton(sound_control_button)
scb_widget.apply_event()
if u.show_messages:
	close_tip = fantas.HoverMessage(sound_control_button, '静音', u.hovermessagebox)
	start_tip = fantas.HoverMessage(sound_control_button, '关闭静音', u.hovermessagebox)
	close_tip.apply_event()

def mute():
	sound_control_button.text = chr(0xe903)
	sound_control_button.update_img()
	scb_widget.bind(unmute)
	if u.show_messages:
		close_tip.cancel_event()
		start_tip.apply_event()
	music_processbar.mute()
	sound_processbar.mute()
	u.userdata['music_volume'] = music_processbar.temp_volume
	u.userdata['sound_volume'] = sound_processbar.temp_volume
	u.userdata['muted'] = True
scb_widget.bind(mute)

def unmute(link=True):
	sound_control_button.text = chr(0xe902)
	sound_control_button.update_img()
	u.userdata['music_volume'] = music_processbar.get_data()
	u.userdata['sound_volume'] = sound_processbar.get_data()
	u.userdata['muted'] = False
	scb_widget.bind(mute)
	if u.show_messages:
		start_tip.cancel_event()
		close_tip.apply_event()
	if link:
		music_processbar.unmute()
		sound_processbar.unmute()


def place_element(father):
	sound_control_button.join(father)


def set_music_volume(data):
	pygame.mixer.music.set_volume(data)

def set_sound_volume(data):
	for s in u.sound:
		u.sound[s].set_volume(data)

bgm_channel = pygame.mixer.Channel(1)
def play_music(music):
	bgm_channel.play(u.music[music], -1)

def stop_music():
	bgm_channel.stop()

def pause_music():
	bgm_channel.pause()

def unpause_music():
	bgm_channel.unpause()

def fadeout(time):
	t = threading.Thread(target=bgm_channel.fadeout, args=(time,))
	t.daemon = True
	t.start()

def play_sound(sound):
	u.sound[sound].play()
