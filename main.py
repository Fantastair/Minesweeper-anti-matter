try:
	import pygame
	import subprocess
	from tempfile import NamedTemporaryFile

	import fantas
	from fantas import uimanager as u
	from pathlib import Path

	u.init((1280, 720), r=1)
	u.font, u.image, u.music, u.sound, u.color = fantas.load_merged_res('resource')
	u.color = u.color['color']
	u.version = '1.3'
	subprocess.Popen(['updater.exe', u.version], creationflags=subprocess.CREATE_NEW_CONSOLE)
	pygame.display.set_icon(u.image['icon'])
	pygame.display.set_caption('扫雷（反物质版） V1.3')

	if Path('userdata').exists():
		u.userdata = fantas.load('userdata')
	else:
		import safedata
		u.userdata = safedata.data
		fantas.dump(u.userdata, 'userdata')
	u.userdata['use_cheat'] = False

	u.show_messages = u.userdata['show_hovermessage']

	import style
	if u.show_messages:
		u.hovermessagebox = fantas.HoverMessageBox(3, 30, u.font['shuhei'], style.hovermessage_text, bd=2, bg=u.color['TEXTWHITE'], sc=u.color['TEXTGRAY'], radius={'border_radius': 4})

	import start_ani

	if u.userdata['skip_startani']:
		start_ani.fast_main()
	else:
		start_ani.main()

	import element.music_play as music_play
	import element.ensure as ensure
	import element.game_time as game_time

	def quit():
		if ensure.quit_bg_cover.is_root():
			if u.userdata['close_directly']:
				ensure.quit()
			else:
				if game_time.time_ticker.is_launched():
					game_time.time_ticker.stop()
				ensure.ensure_quit(fantas.Ui(u.screen.copy()), u.root)
				music_play.pause_music()
		elif not u.userdata['close_directly']:
			ensure.requit()

	u.mainloop(quit=quit)
except Exception:
	import traceback
	import element.ensure as ensure
	subprocess.Popen(['crash.exe', traceback.format_exc()], creationflags=subprocess.CREATE_NEW_CONSOLE)
	ensure.quit()
