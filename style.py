import pygame
import pygame.freetype
from fantas import uimanager as u

c = u.color

bf1 = pygame.Color('#323232')  # 按钮的反馈变色幅度
bf2 = pygame.Color('#505050')

gamename_text = {
	'size': 60,
	'fgcolor': c['TEXTWHITE'],
}

gameversion_text = {
	'size': 90,
	'fgcolor': c['TEXTWHITE'],
}

author_text = {
	'size': 30,
	'fgcolor': c['TEXTWHITE'],
}

wb_text = {
	'size': 100,
	'fgcolor': c['TEXTWHITE'],
}

startgame_button = {
	'origin_bg': c['BUTTONBGBLUE'],
	'origin_bd': 2,
	'origin_sc': c['BUTTONBDBLUE'],
	'hover_bg': c['BUTTONBGBLUE']+bf1,
	'hover_bd': 5,
	'hover_sc': c['BUTTONBDBLUE']+bf1,
	'press_bg': c['BUTTONBGBLUE']-bf1,
	'press_bd': 5,
	'press_sc': c['BUTTONBDBLUE']-bf1,
}
startgame_button['press_bg'].a = 255
startgame_button['press_sc'].a = 255

startgame_text = {
	'size': 40,
	'fgcolor': c['TEXTGRAY']
}

clock_icontext = {
	'size': 30,
	'fgcolor': c['TEXTWHITE']
}

clock_text = {
	'size': 25,
	'fgcolor': c['TEXTWHITE']
}
sound_icontext = {
	'size': 30,
	'fgcolor': c['TEXTWHITE']
}

pull_button = {
	'origin_bg': c['TIPGRAY'],
	'origin_bd': 2,
	'origin_sc': c['TEXTWHITE'],
	'hover_bg': c['BUTTONBGBLUE']+bf1,
	'hover_bd': 5,
	'hover_sc': c['TIPBD']+bf1,
	'': c['BUTTONBGBLUE']-bf1,
	'presspress_bg_bd': 5,
	'press_sc': c['TIPBD']-bf1,
}
pull_button['press_bg'].a = 255
pull_button['press_sc'].a = 255

arrow_icontext = {
	'size': 30,
	'fgcolor': c['TEXTWHITE'],
}

introduce_title = {
	'size': 40,
	'fgcolor': c['TEXTWHITE'],
}
introduce_text = {
	'size': 24,
	'fgcolor': c['TEXTWHITE'],
}
hovermessage_text = {
	'size': 14,
	'fgcolor': c['TEXTGRAY'],
}

recommand_text = {
	'size': 13,
	'fgcolor': c['TEXTWHITE'],
}

choose_text = {
	'size': 19,
	'fgcolor': c['TEXTWHITE'],
}
choose_title = {
	'size': 30,
	'fgcolor': c['TEXTGRAY'],
}

musicset_processbar = {
	'origin_bg': c['BUTTONBGBLUE'],
	'set_bg': c['BUTTONBDBLUE'],
}

processbar_num = {
	'size': 12,
	'fgcolor': c['TEXTWHITE'],
}

settings_text1 = {
	'size': 18,
	'fgcolor': c['BUTTONBDBLUE'],
}

settings_text2 = {
	'size': 20,
	'fgcolor': c['TEXTWHITE'],
}


record_title = {
	'size': 36,
	'fgcolor': c['TEXTWHITE'],
}


tickbox = {
	'origin_bg': None,
	'origin_bd': 3,
	'origin_sc': c['TEXTWHITE'],
	'chose_bg': c['BUTTONBGBLUE'],
	'chose_sc': c['BUTTONBDBLUE'],
}

quit_ensure_button = {
	'origin_bg': c['QUITRED'],
	'origin_bd': 2,
	'origin_sc': c['BUTTONBDBLUE'],
	'hover_bg': c['QUITRED']+bf1,
	'hover_bd': 5,
	'hover_sc': c['BUTTONBDBLUE']+bf1,
	'press_bg': c['QUITRED']-bf1,
	'press_bd': 5,
	'press_sc': c['BUTTONBDBLUE']-bf1,
}
quit_ensure_button['press_bg'].a = 255
quit_ensure_button['press_sc'].a = 255

quit_cancel_button = {
	'origin_bg': None,
	'origin_bd': 2,
	'origin_sc': c['BUTTONBDBLUE'],
	'hover_bg': None,
	'hover_bd': 5,
	'hover_sc': c['BUTTONBDBLUE']+bf1,
	'press_bg': None,
	'press_bd': 5,
	'press_sc': c['BUTTONBDBLUE']-bf1,
}
quit_cancel_button['press_sc'].a = 255

quit_title = {
	'fgcolor': c['TEXTWHITE'],
	'size': 40,
}

quit_text = {
	'fgcolor': c['TEXTGRAY'],
	'size': 26,
}

quit_text_small = {
	'fgcolor': c['TEXTGRAY'],
	'size': 20,
}


map_text = {
	'fgcolor': c['TEXTWHITE'],
	'size': 24,
}


map_data = {
	'fgcolor': c['TEXTWHITE'],
	'size': 20,
}


lostwin_text = {
	'fgcolor': c['TEXTWHITE'],
	'size': 80,
	'style': pygame.freetype.STYLE_STRONG
}

playagain_text = {
	'fgcolor': c['TEXTGRAY'],
	'size': 30,
}
